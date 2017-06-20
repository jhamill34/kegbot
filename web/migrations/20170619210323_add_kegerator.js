'use strict'

exports.up = function (knex, Promise) {
  return knex.schema.createTable('kegerator', function (table) {
    table.increments()
    table.integer('max_kegs')
    table.timestamps(true, true)
  })
}

exports.down = function (knex, Promise) {
  return knex.schema.dropTable('kegerator')
}
