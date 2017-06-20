'use strict'

exports.seed = function(knex, Promise) {
  // Deletes ALL existing entries
  return knex('users').del()
    .then(function () {
      // Inserts seed entries
      return knex('users').insert([
        {name: 'Josh',    rfid: '64,84,139,25', tokens: 5},
        {name: 'Ty',      rfid: '80,77,34,25',  tokens: 3},
        {name: 'Robert',  rfid: '6,4,136,187',  tokens: 1},
        {name: 'Brittany',rfid: '149,6,90,190', tokens: 1},
      ]);
    });
};
