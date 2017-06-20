'use strict'

const AbstractController = require('./abstract_router')

class UserController extends AbstractController{
  constructor (table, knex) {
    super()
    this.knex = knex
  }

  // Override
  index (req, res) {
    this.knex('users').then((users) => {
      res.json(users)
    })
  }

  // Override
  show (req, res) {
    this.knex('users').where('id', '=', req.params.id).limit(1).then((user) => {
      res.json(user)
    });
  }
}

module.exports = UserController
