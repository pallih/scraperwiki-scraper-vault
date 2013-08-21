[
  {
    "op": "core/column-split",
    "description": "Split column key by separator",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "key",
    "guessCellType": true,
    "removeOriginalColumn": true,
    "mode": "separator",
    "separator": ":",
    "regex": false,
    "maxColumns": 0
  },
  {
    "op": "core/column-rename",
    "description": "Rename column key 1 to page",
    "oldColumnName": "key 1",
    "newColumnName": "page"
  },
  {
    "op": "core/column-rename",
    "description": "Rename column key 2 to top",
    "oldColumnName": "key 2",
    "newColumnName": "top"
  },
  {
    "op": "core/column-reorder",
    "description": "Reorder columns",
    "columnNames": [
      "page",
      "top",
      "line"
    ]
  },
  {
    "op": "core/row-reorder",
    "description": "Reorder rows",
    "mode": "record-based",
    "sorting": {
      "criteria": [
        {
          "reverse": false,
          "column": "page",
          "valueType": "number",
          "blankPosition": 2,
          "errorPosition": 1
        },
        {
          "reverse": false,
          "column": "top",
          "valueType": "number",
          "blankPosition": 2,
          "errorPosition": 1
        }
      ]
    }
  },
  {
    "op": "core/text-transform",
    "description": "Text transform on cells in column line using expression grel:value.replace(\"&#160;\", \" \")",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "line",
    "expression": "grel:value.replace(\"&#160;\", \" \")",
    "onError": "set-to-blank",
    "repeat": false,
    "repeatCount": 10
  },
  {
    "op": "core/row-removal",
    "description": "Remove rows",
    "engineConfig": {
      "facets": [
        {
          "expression": "value",
          "to": 100,
          "selectError": true,
          "selectNumeric": true,
          "name": "top",
          "selectBlank": true,
          "columnName": "top",
          "selectNonNumeric": true,
          "from": 20,
          "type": "range"
        }
      ],
      "mode": "row-based"
    }
  },
  {
    "op": "core/row-removal",
    "description": "Remove rows",
    "engineConfig": {
      "facets": [
        {
          "expression": "value",
          "invert": false,
          "selectError": false,
          "omitError": false,
          "name": "page",
          "selectBlank": false,
          "columnName": "page",
          "omitBlank": false,
          "type": "list",
          "selection": [
            {
              "v": {
                "v": 1,
                "l": "1"
              }
            }
          ]
        },
        {
          "expression": "value",
          "to": 160,
          "selectError": true,
          "selectNumeric": true,
          "name": "top",
          "selectBlank": true,
          "columnName": "top",
          "selectNonNumeric": true,
          "from": 20,
          "type": "range"
        }
      ],
      "mode": "row-based"
    }
  },
  {
    "op": "core/row-removal",
    "description": "Remove rows",
    "engineConfig": {
      "facets": [
        {
          "expression": "value",
          "to": 600,
          "selectError": true,
          "selectNumeric": true,
          "name": "top",
          "selectBlank": true,
          "columnName": "top",
          "selectNonNumeric": true,
          "from": 590,
          "type": "range"
        }
      ],
      "mode": "row-based"
    }
  },
  {
    "op": "core/text-transform",
    "description": "Text transform on cells in column line using expression grel:forEach(value[2,-2].split(\"), (\"), v, v.partition(\", \", true).join(\":\")).join(\" | \")",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "line",
    "expression": "grel:forEach(value[2,-2].split(\"), (\"), v, v.partition(\", \", true).join(\":\")).join(\" | \")",
    "onError": "set-to-blank",
    "repeat": false,
    "repeatCount": 10
  },
  {
    "op": "core/column-addition",
    "description": "Create column Paid Entity Name at index 3 based on column line using expression grel:filter(value.split(\" | \"), v, v.split(\":\")[0].toNumber() < 20)[0][4,-1].unescape(\"html\")",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "newColumnName": "Paid Entity Name",
    "columnInsertIndex": 3,
    "baseColumnName": "line",
    "expression": "grel:filter(value.split(\" | \"), v, v.split(\":\")[0].toNumber() < 20)[0][4,-1].unescape(\"html\")",
    "onError": "set-to-blank"
  },
  {
    "op": "core/column-addition",
    "description": "Create column Paid Entity Location at index 3 based on column line using expression grel:filter(value.split(\" | \"), v, v.startsWith(\"236:\"))[0][5,-1].unescape(\"html\")",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "newColumnName": "Paid Entity Location",
    "columnInsertIndex": 3,
    "baseColumnName": "line",
    "expression": "grel:filter(value.split(\" | \"), v, v.startsWith(\"236:\"))[0][5,-1].unescape(\"html\")",
    "onError": "set-to-blank"
  },
  {
    "op": "core/column-addition",
    "description": "Create column Paid Entity State at index 3 based on column line using expression grel:filter(value.split(\" | \"), v, v.startsWith(\"322:\"))[0][5,-1].unescape(\"html\")",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "newColumnName": "Paid Entity State",
    "columnInsertIndex": 3,
    "baseColumnName": "line",
    "expression": "grel:filter(value.split(\" | \"), v, v.startsWith(\"322:\"))[0][5,-1].unescape(\"html\")",
    "onError": "set-to-blank"
  },
  {
    "op": "core/column-addition",
    "description": "Create column Provider of Service at index 3 based on column line using expression grel:filter(value.split(\" | \"), v, v.startsWith(\"347:\"))[0][5,-1].unescape(\"html\")",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "newColumnName": "Provider of Service",
    "columnInsertIndex": 3,
    "baseColumnName": "line",
    "expression": "grel:filter(value.split(\" | \"), v, v.startsWith(\"347:\"))[0][5,-1].unescape(\"html\")",
    "onError": "set-to-blank"
  },
  {
    "op": "core/text-transform",
    "description": "Text transform on cells in column line using expression grel:filter(value.split(\" | \"), v, v.partition(\":\")[0].toNumber() > 347).join(\" | \")",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "line",
    "expression": "grel:filter(value.split(\" | \"), v, v.partition(\":\")[0].toNumber() > 347).join(\" | \")",
    "onError": "set-to-blank",
    "repeat": false,
    "repeatCount": 10
  },
  {
    "op": "core/column-reorder",
    "description": "Reorder columns",
    "columnNames": [
      "page",
      "top",
      "Paid Entity Name",
      "Paid Entity Location",
      "Paid Entity State",
      "Provider of Service",
      "line"
    ]
  },
  {
    "op": "core/column-addition",
    "description": "Create column Patient Education Programs at index 7 based on column line using expression grel:filter(value.split(\" | \"), v, v.partition(\":\")[0].toNumber() < 500)[0][5,-1]",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "newColumnName": "Patient Education Programs",
    "columnInsertIndex": 7,
    "baseColumnName": "line",
    "expression": "grel:filter(value.split(\" | \"), v, v.partition(\":\")[0].toNumber() < 500)[0][5,-1]",
    "onError": "set-to-blank"
  },
  {
    "op": "core/text-transform",
    "description": "Text transform on cells in column line using expression grel:filter(value.split(\" | \"), v, v.partition(\":\")[0].toNumber() > 500).join(\" | \")",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "line",
    "expression": "grel:filter(value.split(\" | \"), v, v.partition(\":\")[0].toNumber() > 500).join(\" | \")",
    "onError": "set-to-blank",
    "repeat": false,
    "repeatCount": 10
  },
  {
    "op": "core/column-addition",
    "description": "Create column Healthcare Professional Education Programs at index 7 based on column line using expression grel:filter(value.split(\" | \"), v, v.partition(\":\")[0].toNumber() < 600)[0][5,-1]",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "newColumnName": "Healthcare Professional Education Programs",
    "columnInsertIndex": 7,
    "baseColumnName": "line",
    "expression": "grel:filter(value.split(\" | \"), v, v.partition(\":\")[0].toNumber() < 600)[0][5,-1]",
    "onError": "set-to-blank"
  },
  {
    "op": "core/text-transform",
    "description": "Text transform on cells in column line using expression grel:filter(value.split(\" | \"), v, v.partition(\":\")[0].toNumber() > 550).join(\" | \")",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "line",
    "expression": "grel:filter(value.split(\" | \"), v, v.partition(\":\")[0].toNumber() > 550).join(\" | \")",
    "onError": "set-to-blank",
    "repeat": false,
    "repeatCount": 10
  },
  {
    "op": "core/column-addition",
    "description": "Create column Advising/Consulting & Int Ed Programs at index 7 based on column line using expression grel:filter(value.split(\" | \"), v, v.partition(\":\")[0].toNumber() < 600)[0][5,-1]",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "newColumnName": "Advising/Consulting & Int Ed Programs",
    "columnInsertIndex": 7,
    "baseColumnName": "line",
    "expression": "grel:filter(value.split(\" | \"), v, v.partition(\":\")[0].toNumber() < 600)[0][5,-1]",
    "onError": "set-to-blank"
  },
  {
    "op": "core/text-transform",
    "description": "Text transform on cells in column line using expression grel:filter(value.split(\" | \"), v, v.partition(\":\")[0].toNumber() > 600).join(\" | \")",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "line",
    "expression": "grel:filter(value.split(\" | \"), v, v.partition(\":\")[0].toNumber() > 600).join(\" | \")",
    "onError": "set-to-blank",
    "repeat": false,
    "repeatCount": 10
  },
  {
    "op": "core/column-addition",
    "description": "Create column Certain Travel-Related Expenses at index 7 based on column line using expression grel:filter(value.split(\" | \"), v, v.partition(\":\")[0].toNumber() < 700)[0][5,-1]",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "newColumnName": "Certain Travel-Related Expenses",
    "columnInsertIndex": 7,
    "baseColumnName": "line",
    "expression": "grel:filter(value.split(\" | \"), v, v.partition(\":\")[0].toNumber() < 700)[0][5,-1]",
    "onError": "set-to-blank"
  },
  {
    "op": "core/text-transform",
    "description": "Text transform on cells in column line using expression grel:filter(value.split(\" | \"), v, v.partition(\":\")[0].toNumber() > 650)[0][5,-1]",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "line",
    "expression": "grel:filter(value.split(\" | \"), v, v.partition(\":\")[0].toNumber() > 650)[0][5,-1]",
    "onError": "set-to-blank",
    "repeat": false,
    "repeatCount": 10
  },
  {
    "op": "core/column-rename",
    "description": "Rename column line to Aggregate",
    "oldColumnName": "line",
    "newColumnName": "Aggregate"
  },
  {
    "op": "core/column-reorder",
    "description": "Reorder columns",
    "columnNames": [
      "page",
      "top",
      "Paid Entity Name",
      "Paid Entity Location",
      "Paid Entity State",
      "Provider of Service",
      "Patient Education Programs",
      "Healthcare Professional Education Programs",
      "Advising/Consulting & Int Ed Programs",
      "Certain Travel-Related Expenses",
      "Aggregate"
    ]
  },
  {
    "op": "core/column-addition",
    "description": "Create column top2 at index 2 based on column top using expression grel:round(value / 7) * 7",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "newColumnName": "top2",
    "columnInsertIndex": 2,
    "baseColumnName": "top",
    "expression": "grel:round(value / 7) * 7",
    "onError": "set-to-blank"
  },
  {
    "op": "core/column-reorder",
    "description": "Reorder columns",
    "columnNames": [
      "Paid Entity Name",
      "Paid Entity Location",
      "Paid Entity State",
      "Provider of Service",
      "Patient Education Programs",
      "Healthcare Professional Education Programs",
      "Advising/Consulting & Int Ed Programs",
      "Certain Travel-Related Expenses",
      "Aggregate",
      "page",
      "top",
      "top2"
    ]
  },
  {
    "op": "core/multivalued-cell-join",
    "description": "Join multi-valued cells in column Provider of Service",
    "columnName": "Provider of Service",
    "keyColumnName": "Paid Entity Name",
    "separator": " "
  },
  {
    "op": "core/row-removal",
    "description": "Remove rows",
    "engineConfig": {
      "facets": [
        {
          "invert": false,
          "expression": "isBlank(value)",
          "selectError": false,
          "omitError": false,
          "selectBlank": false,
          "name": "Paid Entity Name",
          "omitBlank": false,
          "columnName": "Paid Entity Name",
          "type": "list",
          "selection": [
            {
              "v": {
                "v": true,
                "l": "true"
              }
            }
          ]
        }
      ],
      "mode": "row-based"
    }
  },
  {
    "op": "core/text-transform",
    "description": "Text transform on cells in column Patient Education Programs using expression grel:value.replace(\",\", \"\").toNumber()",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Patient Education Programs",
    "expression": "grel:value.replace(\",\", \"\").toNumber()",
    "onError": "set-to-blank",
    "repeat": false,
    "repeatCount": 10
  },
  {
    "op": "core/text-transform",
    "description": "Text transform on cells in column Healthcare Professional Education Programs using expression grel:value.replace(\",\", \"\").toNumber()",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Healthcare Professional Education Programs",
    "expression": "grel:value.replace(\",\", \"\").toNumber()",
    "onError": "set-to-blank",
    "repeat": false,
    "repeatCount": 10
  },
  {
    "op": "core/text-transform",
    "description": "Text transform on cells in column Advising/Consulting & Int Ed Programs using expression grel:value.replace(\",\", \"\").toNumber()",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Advising/Consulting & Int Ed Programs",
    "expression": "grel:value.replace(\",\", \"\").toNumber()",
    "onError": "set-to-blank",
    "repeat": false,
    "repeatCount": 10
  },
  {
    "op": "core/text-transform",
    "description": "Text transform on cells in column Certain Travel-Related Expenses using expression grel:value.replace(\",\", \"\").toNumber()",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Certain Travel-Related Expenses",
    "expression": "grel:value.replace(\",\", \"\").toNumber()",
    "onError": "set-to-blank",
    "repeat": false,
    "repeatCount": 10
  },
  {
    "op": "core/text-transform",
    "description": "Text transform on cells in column Aggregate using expression grel:value.replace(\",\", \"\").toNumber()",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Aggregate",
    "expression": "grel:value.replace(\",\", \"\").toNumber()",
    "onError": "set-to-blank",
    "repeat": false,
    "repeatCount": 10
  },
  {
    "op": "core/mass-edit",
    "description": "Mass edit cells in column Paid Entity Name",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Paid Entity Name",
    "expression": "value",
    "edits": [
      {
        "fromBlank": false,
        "fromError": false,
        "from": [
          "PSYCHIATRIC SOLUTIONS",
          "PSYCHIATRIC SOLUTIONS."
        ],
        "to": "PSYCHIATRIC SOLUTIONS"
      }
    ]
  }
]