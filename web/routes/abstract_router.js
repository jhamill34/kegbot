const express = require('express')
const Joi = require('joi')

class AbstractController {
  constructor () {
    this.router = express.Router()
  }

  getRouter () {
    this.router.get('/', this.index.bind(this))
    this.router.get('/:id', this.show.bind(this))
    this.router.put('/:id', this.update.bind(this))
    this.router.post('/', this.create.bind(this))
    this.router.delete('/:id', this.delete.bind(this))
    return this.router
  }

  verify (obj) {
    return Joi.validate(obj, this.schema)
  }

  index (req, res) {
    res.sendStatus(404);
  }
  show (req, res) {
    res.sendStatus(404);
  }
  update (req, res) {
    res.sendStatus(404);
  }
  delete (req, res) {
    res.sendStatus(404);
  }
  create (req, res) {
    res.sendStatus(404);
  }
}

module.exports = AbstractController
