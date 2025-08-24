{
  "name": "Earnings + Announcements + MoneyControl Merge",
  "nodes": [
    {
      "parameters": {
        "triggerTimes": {
          "item": [
            {
              "mode": "everyHour"
            }
          ]
        }
      },
      "id": "1",
      "name": "Cron Trigger",
      "type": "n8n-nodes-base.cron",
      "typeVersion": 1,
      "position": [
        200,
        300
      ]
    },
    {
      "parameters": {
        "url": "http://host.docker.internal/earnings",
        "method": "GET"
      },
      "id": "2",
      "name": "Earnings",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 1,
      "position": [
        450,
        150
      ]
    },
    {
      "parameters": {
        "url": "http://host.docker.internal/announcements",
        "method": "GET"
      },
      "id": "3",
      "name": "Announcements",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 1,
      "position": [
        450,
        300
      ]
    },
    {
      "parameters": {
        "url": "http://host.docker.internal/moneycontrol",
        "method": "GET"
      },
      "id": "4",
      "name": "Money Control",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 1,
      "position": [
        450,
        450
      ]
    },
    {
      "parameters": {
        "mode": "append"
      },
      "id": "5",
      "name": "Merge A+B",
      "type": "n8n-nodes-base.merge",
      "typeVersion": 1,
      "position": [
        700,
        220
      ]
    },
    {
      "parameters": {
        "mode": "append"
      },
      "id": "6",
      "name": "Merge (A+B)+C",
      "type": "n8n-nodes-base.merge",
      "typeVersion": 1,
      "position": [
        950,
        300
      ]
    },
    {
      "parameters": {
        "functionCode": "return [{ json: { data: items.map(item => item.json) } }];"
      },
      "id": "7",
      "name": "Prepare Array",
      "type": "n8n-nodes-base.function",
      "typeVersion": 1,
      "position": [
        1200,
        300
      ]
    },
    {
      "parameters": {
        "url": "http://host.docker.internal/final-endpoint",
        "method": "POST",
        "jsonParameters": true,
        "options": {},
        "bodyParametersJson": "={{$json}}"
      },
      "id": "8",
      "name": "Send Merged Output",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 1,
      "position": [
        1450,
        300
      ]
    }
  ],
  "connections": {
    "1": {
      "main": [
        [
          {
            "node": "2",
            "type": "main",
            "index": 0
          },
          {
            "node": "3",
            "type": "main",
            "index": 0
          },
          {
            "node": "4",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "2": {
      "main": [
        [
          {
            "node": "5",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "3": {
      "main": [
        [
          {
            "node": "5",
            "type": "main",
            "index": 1
          }
        ]
      ]
    },
    "4": {
      "main": [
        [
          {
            "node": "6",
            "type": "main",
            "index": 1
          }
        ]
      ]
    },
    "5": {
      "main": [
        [
          {
            "node": "6",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "6": {
      "main": [
        [
          {
            "node": "7",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "7": {
      "main": [
        [
          {
            "node": "8",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  }
}
