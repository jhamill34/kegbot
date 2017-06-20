'use strict'

exports.up = function (knex, Promise) {
  return knex.schema.createTable('keg', function (table) {
    table.increments()
    table.decimal('pints')
    table.decimal('starting_pints')
    table.timestamp('deleted_at')
    table.integer('beer_id').references('beer.id')
    table.integer('kegerator_id').references('kegerator.id')
    table.timestamps(true, true)
  })
}

exports.down = function (knex, Promise) {
  return knex.schema.dropTable('keg')
}
