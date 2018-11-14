var express = require("express");
require('dotenv').config()

const { Pool, Client } = require('pg')
const pool = new Pool()
var genelDurum = {}

function monthFunction() {
    var months = ['ocak', 'subat', 'mart', 'nisan', 'mayıs', 'haziran',
        'temmuz', 'agustos', 'eylul', 'ekim', 'kasım', 'aralık'];
    var d = new Date();
    var n = d.getMonth() - 1;

    return months[n];
}
thisMonth = monthFunction();

//Genel 
pool.query(`select row_to_json(r) from (select grup, miktar from ${thisMonth}_rapor) r;`, (err, res) => {
    genelDurum = res;
})

pool.query(`select row_to_json(r) from (select degisken, miktar from ${thisMonth}_rapor_ayrinti where etiket = 'priority') r;`, (err, res) => {
    genelDurumPri = res;
})

pool.query(`select row_to_json(r) from (select degisken, miktar from ${thisMonth}_rapor_ayrinti where etiket = 'state') r;`, (err, res) => {
    genelDurumSt = res;
})

pool.query(`select row_to_json(r) from (select degisken, miktar from ${thisMonth}_rapor_ayrinti where etiket = 'project') r;`, (err, res) => {
    genelDurumPrj = res;
})

pool.query(`select row_to_json(r) from (select degisken, miktar from ${thisMonth}_rapor_ayrinti where etiket = 'assignee') r`, (err, res) => {
    genelDurumAssg = res;
})

pool.query(`select row_to_json(r) from (select degisken, miktar from ${thisMonth}_rapor_ayrinti where etiket = 'user_mean' order by miktar) r`, (err, res) => {
    genelDurumMeans = res;
})

//Ankara 
pool.query(`select row_to_json(r) from (select degisken, miktar from ${thisMonth}_ank_ayrinti where etiket = 'priority') r`, (err, res) => {
    ankaraPri = res;
})

pool.query(`select row_to_json(r) from (select degisken, miktar from ${thisMonth}_ank_ayrinti where etiket = 'state') r`, (err, res) => {
    ankaraState = res;
})

pool.query(`select row_to_json(r) from (select degisken, miktar from ${thisMonth}_ank_ayrinti where etiket = 'project') r`, (err, res) => {
    ankaraProject = res;
})

pool.query(`select row_to_json(r) from (select degisken, miktar from ${thisMonth}_ank_ayrinti where etiket = 'assignee') r`, (err, res) => {
    ankaraAssignee = res;
})

//İstanbul
pool.query(`select row_to_json(r) from (select degisken, miktar from ${thisMonth}_ist_ayrinti where etiket = 'priority') r`, (err, res) => {
    istPri = res;
})

pool.query(`select row_to_json(r) from (select degisken, miktar from ${thisMonth}_ist_ayrinti where etiket = 'state') r`, (err, res) => {
    istState = res;
})

pool.query(`select row_to_json(r) from (select degisken, miktar from ${thisMonth}_ist_ayrinti where etiket = 'project') r`, (err, res) => {
    istProject = res;
})

pool.query(`select row_to_json(r) from (select degisken, miktar from ${thisMonth}_ist_ayrinti where etiket = 'assignee') r`, (err, res) => {
    istAssignee = res;
})



const client = new Client()
var app = express();
app.set('view engine', 'ejs');
app.get('/', function (req, res) {
    res.render("index", { data1: genelDurum, data10: genelDurumPri, data11: genelDurumSt, data12: genelDurumPrj, data13: genelDurumAssg, data14: genelDurumMeans });
});

app.get('/ankara', function (req, res) {
    res.render("ankara", { data2: ankaraPri, data3: ankaraState, data4: ankaraProject, data5: ankaraAssignee })
});

app.get('/istanbul', function (req, res) {
    res.render("istanbul", { data6: istPri, data7: istState, data8: istProject, data9: istAssignee })
});

app.listen(process.env.PORT || 3000, function () {
    console.log("Server Started!");
})
app.use(express.static(__dirname + '/charts'));