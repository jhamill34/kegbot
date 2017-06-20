'use strict'

exports.up = function (knex, Promise) {
  return knex.schema.createTable('users', function (table) {
    table.increments()
    table.string('rfid').unique()
    table.string('name')
    table.integer('tokens')
    table.timestamps(true, true)
  })
}

exports.down = function (knex, Promise) {
  return knex.schema.dropTable('users')
}
