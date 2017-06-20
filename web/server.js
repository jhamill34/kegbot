'use strict'

const express = require('express')
const KegController = require('./routes/keg_routes')
const UserController = require('./routes/user_routes')

const app = express()
const http = require('http').Server(app)

const dbconfig = require('./knexfile')[process.env.NODE_ENV || 'development']
const knex = require('knex')(dbconfig)

const bodyParser = require('body-parser')

app.use(bodyParser.json())

app.use('/kegs', new KegController('kegs', knex).getRouter())
app.use('/users', new UserController('users', knex).getRouter())

module.exports = http
