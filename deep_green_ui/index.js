var express = require('express');
var bodyParser = require('body-parser');
var path = require('path');

var app = express();

// Middle ware
var logger = function (req, res, next) {
    console.log('Logging...');
    next();
}

// Body parser middleware
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));

// Set Static path
app.use(express.static(path.join(__dirname, 'public')));

app.engine('.html', require('ejs').__express);

// Optional since express defaults to CWD/views

app.set('views', path.join(__dirname, 'views'));

// Without this you would need to
// supply the extension to res.render()
// ex: res.render('users.html').
app.set('view engine', 'html');

app.use(logger);

// Dummy users
var users = [
    { name: 'tobi', email: 'tobi@learnboost.com' },
    { name: 'loki', email: 'loki@learnboost.com' },
    { name: 'jane', email: 'jane@learnboost.com' }
];

// Mock columns
var credit_columns = [
    { name: 'age', data_type: 'continous' },
    { name: 'income', data_type: 'continous' },
    { name: 'gender', data_type: 'categorical' },
]


app.get('/', function (req, res) {
    console.log('sdfasdf');
});

// Database Columns
app.get('/database_columns', function (req, res) {
    res.render('db_columns', {
        database_columns: credit_columns,
        title: "Credit Scoring Columns",
    });
});

app.post('/database_columns', function (req, res) {
    console.log(req.body);
});

// Connection String and Choose Table

// Mock connection string
var connection_string = [
    { name: 'Server', content: 'omnervos' },
    { name: 'Database', content: 'bananna' },
    { name: 'User Name', content: 'Admin.Green' },
    { name: 'Password', content: 'lalala' },
]

// Mock table list
var table_list = [
    { name: "Credit Scoring" },
    { name: "Flower Prediction" },
    { name: "Party" },
    { name: "Contract" },
]

app.get('/connection_string', function (req, res) {
    res.render('connection_string', {
        connection_string: connection_string,
        title: "Get Connection String",
        table_list: table_list,
    });
});

app.post('/connection_string', function (req, res) {
    console.log(req.body);

    var newList = [
        { name: "Daisy" },
        { name: "Flower" },
    ]
    // res.send( { table_list : newList } )
});

app.get('/connection_string/submit', function (req, res) {
    console.log(req.body);

    var newList = [
        { name: "Daisy" },
        { name: "Flower" },
    ]
    req.send( { table_list : newList } )
});

// app.post('/selected_table', function (req, res) {
//     console.log(req.body);
//     res.render('db_columns', {
//         database_columns: credit_columns,
//         title: req.body.table,
//     });
// });

// Middle ware that can unhide the div
var unhideDiv = function (req, res) {

}

app.post('/selected_table', function (req, res) {
    console.log(req.body);
    req.body.database_columns
});


// Display Model

// Mock model details
var model_detail = [
    { name: 'accuracy', value: '98%' },
    { name: 'weight', value: '0.7' },
    { name: 'biases', value: '16' },
]

app.get('/display_model', function (req, res) {
    res.render('display_model', {
        model_detail: model_detail,
        title: "Credit Scoring"
    });
});


// Predict Model
app.get('/predict_model', function (req, res) {
    res.render('predict_model', {
        database_columns: credit_columns,
        title: "Credit Scoring"
    });
});

app.post('/predict_model', function (req, res) {
    console.log(req.body);
});

// Try Render
app.get('/test', function (req, res) {
    res.render('test');
});


// Try Render
app.get('/default', function (req, res) {
    res.render('default', {
        title: "Credit Scoring",
        model_detail: model_detail,
        connection_string: connection_string,
        database_columns: credit_columns,
        table_list: table_list,
    });
});



app.listen(3000, function () {
    console.log('Server starting at port 3000...');
});