// This file is part of InvenioRDM
// Copyright (C) 2020 CERN.
// Copyright (C) 2020 Northwestern University.
//
// Invenio App RDM is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import React from "react";
import ReactDOM from "react-dom";
import "semantic-ui-css/semantic.min.css";
import { i18next } from "./i18next";
import { getInputFromDOM } from "react-invenio-deposit";
import { RDMDepositForm } from "./RDMDepositForm";

ReactDOM.render(
  <RDMDepositForm
    record={getInputFromDOM("deposits-record")}
    files={getInputFromDOM("deposits-record-files")}
    config={getInputFromDOM("deposits-config")}
    permissions={getInputFromDOM("deposits-record-permissions")}
  />,
  document.getElementById("deposit-form")
);

document.getElementsByClassName("save-button")[0]
        .addEventListener("click", function() {
          const embargoDate = new Date(document.getElementById("access.embargo.until").value)   // YYYY-MM-DD
          const today = new Date()

          if((embargoDate - today) / (1000 * 3600 * 24*365) > 1 ) {
            document.getElementsByName("publish")[0].disabled = true;
            alert("Embargo Date cannot be greater than 1 year from now.");
          }
        })