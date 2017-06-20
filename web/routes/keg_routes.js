'use strict'

const AbstractController = require('./abstract_router')
const Joi = require('joi')

class KegController extends AbstractController{
  constructor (table, knex) {
    super()
    this.knex = knex
    this.schema = Joi.object().keys({
      id: Joi.number().integer(),
      name: Joi.string().alphanum(),
      pints: Joi.number().min(0).max(Joi.ref('starting_pints')),
      starting_pints: Joi.number().greater(0)
    })
  }

  // Override
  index (req, res) {
    this.knex('kegs').whereNull('deleted_at').then((kegs) => {
      res.json(kegs)
    })
  }

  // Override
  show (req, res) {
    this.knex('kegs')
      .whereNull('deleted_at')
      .andWhere('id', '=', req.params.id)
      .limit(1)
      .then(([keg]) => {
        res.json(keg)
      });
  }

  // Override
  update (req, res) {
    let result = this.verify(req.body)
    if(result.error !== null) {
      Object.assign(result.value, {
        updated_at: 'now()'
      })

      this.knex('kegs').where('id', '=', req.params.id)
        .update(result.value).then(() => {
          res.status(204).json()
        })
        .catch(() => {
          res.sendStatus(500)
        })
    } else {
      res.json(result.error)
    }
  }

  // Override
  create (req, res) {
    let result = this.verify(req.body)
    if(result.error !== null) {
      Object.assign(result.value, {
        created_at: 'now()',
        updated_at: 'now()',
        deleted_at: null
      })

      this.knex('kegs').insert(result.value)
        .returning(['id', 'created_at', 'updated_at'])
        .then(([returning]) => {
          let persistedValue = Object.assign({}, result.value, returning)
          res.status(201).json(persistedValue)
        })
        .catch(() => {
          res.sendStatus(500)
        })
    } else {
      res.json(result.error)
    }
  }

  // Override
  delete (req, res) {
    this.knex('kegs').where('id', '=', req.params.id)
      .update({
        deleted_at: 'now()'
      })
      .then((count) => {
        res.sendStatus(204)
      })
      .catch(() => {
        res.sendStatus(500)
      })
  }
}

module.exports = KegController
