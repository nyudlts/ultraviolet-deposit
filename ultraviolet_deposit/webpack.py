# -*- coding: utf-8 -*-
#
# Copyright (C) 2019-2021 CERN.
# Copyright (C) 2019-2021 Northwestern University.
# Copyright (C)      2021 TU Wien.
#
# Invenio App RDM is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""JS/CSS Webpack bundles for theme."""

from invenio_assets.webpack import WebpackThemeBundle

ultraviolet = WebpackThemeBundle(
    __name__,
    'assets',
    default='semantic-ui',
    themes={
        'semantic-ui': dict(
            entry={
                'ultraviolet-deposit':
                    './js/ultraviolet/index.js',
            },
            dependencies={
                # add any additional npm dependencies here...
                "@babel/runtime": "^7.9.0",
                "axios": "^0.21.1",
                "formik": "^2.1.4",
                "react": "^16.13.1",
                "react-dom": "^16.13.1",
                "react-dropzone": "^11.0.3",
                "react-invenio-forms": "^0.8.0",
                "react-redux": "^7.2",
                "redux": "^4.0.5",
                "redux-thunk": "^2.3.0",
                "lodash": "^4.17.15",
                "semantic-ui-react": "^0.88.0",
                "semantic-ui-css": "^2.4.1",
                "i18next": "^20.3.1",
                "i18next-browser-languagedetector": "^6.1.1",
                "react-i18next": "^11.11.3",
                'luxon': '^1.23.0',
                'path': '^0.12.7',
                'prop-types': '^15.7.2',
                'react-dnd': '^11.1.3',
                'react-dnd-html5-backend': '^11.1.3',
                'react-invenio-deposit': '^0.17.0',
                'react-ultraviolet-deposit': '^0.0.3',
                'yup': '^0.32.9',
                '@ckeditor/ckeditor5-build-classic': '^16.0.0',
                '@ckeditor/ckeditor5-react': '^2.1.0',
                'react-copy-to-clipboard': '^5.0.3',
                'jquery': '^3.2.1',
            },
        ),
    }
)