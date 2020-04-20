const fetch = require("node-fetch");
//const response = fetch("http://127.0.0.1:5000/login?username=username&password=password").then(e => e.json()).then(e => console.log(e));
//const response = fetch("http://127.0.0.1:5000/get_shared_trans?groupID=1").then(e => e.json()).then(e => console.log(e));
/*
const response = fetch("http://127.0.0.1:5000/put_trans", {
    method: "PUT",
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ 
        "transaction": {
            "transactionID": "5923",
            "paidBy": "CHANGED",
            "description": "Breakfast",
            //"postingDateTime": "2020-03-03",
            //"amount": "96.90",
            //"merchantName": "Brunch Co",
            "merchantCatergoryCode": "5812",
            "breakdown": {
                "Michael": "0.25",
                "Bianca": "0.25",
                "John": "0.25",
                "Bob": "0.25"
            },
            "disputeStatus": {
                "Michael": false,
                "Bianca": false,
                "John": false,
                "Bob": false
            },
            "notes": ""
        }, 
        "groupID": 2 
    })
}).then(e => e.json()).then(e => console.log(e));
*/
const response = fetch("http://127.0.0.1:5000/get_users?groupID=1").then(e => e.json()).then(e => console.log(e));
//const response = fetch("http://127.0.0.1:5000/get_rules?groupID=1").then(e => e.json()).then(e => console.log(e));
//const response = fetch("http://127.0.0.1:5000/get_personal_trans").then(e => e.json()).then(e => console.log(e));
//const response = fetch("http://127.0.0.1:5000/get_stats?groupID=1").then(e => e.json()).then(e => console.log(e));
//const response = fetch("http://127.0.0.1:5000/get_total?groupID=2").then(e => e.json()).then(e => console.log(e));