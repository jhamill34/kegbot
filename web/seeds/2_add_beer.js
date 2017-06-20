'use strict'

function cleanBeer (knex) {
  return knex('keg').del()
    .then(function () {
      return knex('kegerator').del()
    })
    .then(function () {
      return knex('beer').del()
    })
}

exports.seed = function(knex, Promise) {
  // Deletes ALL existing entries
  return cleanBeer(knex)
    .then(function () {
      // Inserts seed entries
      return knex('beer').insert([
        {name: 'Old Porter'},
        {name: 'IPA'},
        {name: 'Amber Ale'}
      ])
    })
    .then(function () {
      return knex('kegerator').insert([
        {max_kegs: 1}
      ])
    })
    .then(function () {
      return knex('keg').insert([
        {pints: 23.0, starting_pints: 50.0, beer_id: 2, kegerator_id: 1}
      ])
    })
};
