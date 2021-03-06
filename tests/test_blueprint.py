# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 NYU.
#
# Ultraviolet-Deposit is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

""" A Blueprint which is used for rendering deposit form"""
from flask import request

from flask import Blueprint, abort, current_app, render_template
from flask_talisman import Talisman
from flask_babelex import lazy_gettext as _
from flask_login import login_required
from jinja2 import TemplateNotFound

from invenio_app_rdm.records_ui.views import get_scheme_label
from elasticsearch_dsl import Q
from invenio_access.permissions import system_identity
from invenio_i18n.ext import current_i18n
from invenio_rdm_records.proxies import current_rdm_records
from invenio_rdm_records.services.schemas import RDMRecordSchema
from invenio_rdm_records.services.schemas.utils import dump_empty
from invenio_vocabularies.proxies import current_service as vocabulary_service
from invenio_vocabularies.records.models import VocabularyScheme
from marshmallow_utils.fields.babel import gettext_from_dict
from sqlalchemy.orm import load_only
from flask import make_response, jsonify

#Define a view which is used to prepare and display deposit form. It will be used only for testing.
test_deposit = Blueprint('test_deposit', __name__,
                         template_folder='templates', url_prefix='/')

talisman = Talisman()


@test_deposit.route('/test')
@talisman(content_security_policy=[])
def deposit_form():
    try:
        return render_template(
            'test_deposit.html',
            forms_config=get_form_config(createUrl=("/api/records")),
            searchbar_config=dict(searchUrl=get_search_url()),
            record=new_record(),
            files=dict(
                default_preview=None, entries=[], links={}
            ),
        )
    except TemplateNotFound:
        abort(404)


@test_deposit.route('/api/vocabularies/languages')
@talisman(content_security_policy=[])
def return_languages():
    suggestion = request.args.get('suggest')
    hits = {}
    if ('E' in suggestion):
        hits['hits'] = {"hits": [
            {"tags": ["macrolanguage", "living"], "title_l10n": "English", "id": "eng", "props": {"alpha_2": "en"}}],
                        "total": 1}
    else:
        hits['hits'] = {"hits": [], "total": 0}
    response = make_response(jsonify(hits), 200)
    return response

@test_deposit.route('/api/vocabularies/resourcetypes')
@talisman(content_security_policy=[])
def return_resource_types():
    suggestion = request.args.get('suggest')
    hits = {}
    if ('D' in suggestion):
      hits['hits'] = {"hits": [{
            "id": "dataset",
            "icon": "table",
            "props": {
                "csl": "dataset",
                "datacite_general": "Dataset",
                "datacite_type": '',
                "openaire_resourceType": '21',
                "openaire_type": "dataset",
                "eurepo": "info:eu-repo/semantics/other",
                "schema.org": "https://schema.org/Dataset",
                "subtype": '',
                "type": "dataset",
            },
            "title_l10n":  "Dataset",
            "tags": ["depositable", "linkable"],
            "type": "resourcetypes"
        }], "total": 1}
    else:
        hits['hits'] = {"hits": [], "total": 0}
    response = make_response(jsonify(hits), 200)
    return response


@test_deposit.route('/api/vocabularies/relationtypes')
@talisman(content_security_policy=[])
def return_relation_types():
    suggestion = request.args.get('suggest')
    hits = {}
    if ('I' in suggestion):
        hits['hits'] = {"hits": [{"id": "iscitedby",
         "props": {
            "datacite": "IsCitedBy"
          },
        "title_l10n": "Is cited by",
        "type": "relationtypes"}], "total": 1 }
    else:
        hits['hits'] = {"hits": [], "total": 0}
    response = make_response(jsonify(hits), 200)
    return response

# Helper methods minimally needed to build deposit form
def get_form_pids_config():
    """Prepare configuration for the pids field."""
    service = current_rdm_records.records_service
    pids_providers = []
    for scheme, providers in service.config.pids_providers.items():
        can_be_managed = False
        can_be_unmanaged = False
        provider_enabled = False
        for name, provider_attrs in providers.items():
            is_enabled = provider_attrs.get("enabled", True)
            if not provider_enabled and is_enabled:
                provider_enabled = True

            if provider_attrs["system_managed"]:
                can_be_managed = True
            else:
                can_be_unmanaged = True

        # all providers disabled for this scheme
        if not provider_enabled:
            continue

        record_pid_config = current_app.config[
            "RDM_RECORDS_RECORD_PID_SCHEMES"]
        scheme_label = record_pid_config.get(scheme, {}).get("label", scheme)

        pids_provider = {
            "scheme": scheme,
            "pid_label": scheme_label,
            "pid_placeholder": "10.1234/datacite.123456",
            "can_be_managed": can_be_managed,
            "can_be_unmanaged": can_be_unmanaged,
            "btn_label_discard_pid": _("Discard the reserved {scheme_label}")
                .format(scheme_label=scheme_label),
            "btn_label_get_pid": _("Get a {scheme_label} now!")
                .format(scheme_label=scheme_label),
            "managed_help_text": _("Reserve a {scheme_label} or leave this "
                                   "field blank to have one automatically "
                                   "assigned when publishing.")
                .format(scheme_label=scheme_label),
            "unmanaged_help_text": _("Copy and paste here your {scheme_label}")
                .format(scheme_label=scheme_label),
        }
        pids_providers.append(pids_provider)
    return pids_providers


class VocabulariesOptions:
    """Holds React form vocabularies options."""

    def __init__(self):
        """Constructor."""
        self._vocabularies = {}

    # Utilities
    def _get_label(self, hit):
        """Return label (translated title) of hit."""
        return gettext_from_dict(
            hit["title"],
            current_i18n.locale,
            current_app.config.get('BABEL_DEFAULT_LOCALE', 'en')
        )

    def _get_type_subtype_label(self, hit, type_labels):
        """Return (type, subtype) pair for this hit."""
        id_ = hit["id"]
        type_ = hit.get("props", {}).get("type")

        if id_ == type_:
            # dataset-like case
            return (self._get_label(hit), "")
        elif type_ not in type_labels:
            # safety net to generate a valid type, subtype and not break search
            return (self._get_label(hit), "")
        else:
            return (type_labels[type_], self._get_label(hit))

    def _resource_types(self, extra_filter):
        """Dump resource type vocabulary."""
        type_ = 'resourcetypes'
        all_resource_types = vocabulary_service.read_all(
            system_identity,
            fields=["id", "props", "title", "icon"],
            type=type_,
            # Sorry, we have over 100+ resource types entry at NU actually
            max_records=150
        )
        type_labels = {
            hit["id"]: self._get_label(hit)
            for hit in all_resource_types.to_dict()["hits"]["hits"]
        }
        subset_resource_types = vocabulary_service.read_all(
            system_identity,
            fields=["id", "props", "title", "icon"],
            type=type_,
            extra_filter=extra_filter,
            # Sorry, we have over 100+ resource types entry at NU actually
            max_records=150
        )

        return [
            {
                "icon": hit.get("icon", ""),
                "id": hit["id"],
                "subtype_name": self._get_type_subtype_label(hit, type_labels)[1],  # noqa
                "type_name": self._get_type_subtype_label(hit, type_labels)[0],
            } for hit in subset_resource_types.to_dict()["hits"]["hits"]
        ]

    def _dump_vocabulary_w_basic_fields(self, vocabulary_type):
        """Dump vocabulary with id and title field."""
        results = vocabulary_service.read_all(
            system_identity, fields=["id", "title"], type=vocabulary_type)
        return [
            {
                "text": self._get_label(hit),
                "value": hit["id"],
            } for hit in results.to_dict()["hits"]["hits"]
        ]

    # Vocabularies
    def depositable_resource_types(self):
        """Return depositable resource type options (value, label) pairs."""
        self._vocabularies["resource_type"] = (
            self._resource_types(Q('term', tags="depositable"))
        )
        return self._vocabularies["resource_type"]

    def subjects(self):
        """Dump subjects vocabulary (limitTo really)."""
        subjects = (
            VocabularyScheme.query
                .filter_by(parent_id="subjects")
                .options(load_only("id"))
                .all()
        )
        limit_to = [{"text": "All", "value": "all"}]
        # id is human readable and shorter, so we use it
        limit_to += [{"text": s.id, "value": s.id} for s in subjects]

        self._vocabularies["subjects"] = {"limit_to": limit_to}
        return self._vocabularies["subjects"]

    def title_types(self):
        """Dump title type vocabulary."""
        self._vocabularies["titles"] = dict(
            type=self._dump_vocabulary_w_basic_fields('titletypes')
        )
        return self._vocabularies["titles"]

    def creator_roles(self):
        """Dump creators role vocabulary."""
        self._vocabularies["creators"] = dict(
            role=self._dump_vocabulary_w_basic_fields('creatorsroles')
        )
        return self._vocabularies["creators"]

    def contributor_roles(self):
        """Dump contributors role vocabulary."""
        self._vocabularies["contributors"] = dict(
            role=self._dump_vocabulary_w_basic_fields('contributorsroles')
        )
        return self._vocabularies["contributors"]

    def description_types(self):
        """Dump description type vocabulary."""
        self._vocabularies["descriptions"] = dict(
            type=self._dump_vocabulary_w_basic_fields('descriptiontypes')
        )
        return self._vocabularies["descriptions"]

    def date_types(self):
        """Dump date type vocabulary."""
        self._vocabularies["dates"] = dict(
            type=self._dump_vocabulary_w_basic_fields('datetypes')
        )
        return self._vocabularies["dates"]

    def relation_types(self):
        """Dump relation type vocabulary."""
        return self._dump_vocabulary_w_basic_fields('relationtypes')

    def linkable_resource_types(self):
        """Dump linkable resource type vocabulary."""
        return self._resource_types(Q('term', tags="linkable"))

    def identifier_schemes(self):
        """Dump identifiers scheme (fake) vocabulary.

        "Fake" because identifiers scheme is not a vocabulary.
        """
        return [
            {
                "text": get_scheme_label(scheme),
                "value": scheme
            } for scheme in current_app.config.get(
                "RDM_RECORDS_IDENTIFIERS_SCHEMES", {})
        ]

    def identifiers(self):
        """Dump related identifiers vocabulary."""
        self._vocabularies["identifiers"] = {
            "relations": self.relation_types(),
            "resource_type": self.linkable_resource_types(),
            "scheme": self.identifier_schemes()
        }

    def dump(self):
        """Dump into dict."""
        # TODO: Nest vocabularies inside "metadata" key so that frontend dumber
        self.depositable_resource_types()
        self.title_types()
        self.creator_roles()
        self.description_types()
        self.date_types()
        self.contributor_roles()
        self.subjects()
        self.identifiers()
        # We removed
        # vocabularies["relation_type"] = _dump_relation_types_vocabulary()
        return self._vocabularies


def get_form_config(**kwargs):
    """Get the react form configuration."""
    return dict(
        vocabularies=VocabulariesOptions().dump(),
        current_locale=str(current_i18n.locale),
        default_locale=current_app.config.get('BABEL_DEFAULT_LOCALE', 'en'),
        pids=get_form_pids_config(),
        **kwargs
    )


def get_search_url():
    """Get the search URL."""
    # TODO: this should not be used
    return current_app.config["APP_RDM_ROUTES"]["record_search"]


def new_record():
    """Create an empty record with default values."""
    record = dump_empty(RDMRecordSchema)
    record["files"] = {"enabled": True}
    return record
