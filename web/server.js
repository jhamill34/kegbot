'use strict'

const express = require('express')
const KegController = require('./routes/keg_routes')
const UserController = require('./routes/user_routes')

const os = require('os')
const app = express()
const http = require('http').Server(app)

const dbconfig = require('./knexfile')[process.env.NODE_ENV || 'development']
const knex = require('knex')(dbconfig)

knex.migrate.latest().then(function () {
  knex.seed.run()
})

const bodyParser = require('body-parser')

app.use(bodyParser.json())

app.use('/kegs', new KegController('kegs', knex).getRouter())
app.use('/users', new UserController('users', knex).getRouter())

app.get('/guid', function (req, res) {
  res.json({container: os.hostname()})
})

module.exports = http
