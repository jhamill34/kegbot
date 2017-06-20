// Update with your config settings.

module.exports = {
  development: {
    client: 'postgresql',
    connection: {
      host: '172.20.0.2',
      database: 'kegbot',
      user:     'docker',
      password: 'mysecretpassword'
    },
    pool: {
      min: 2,
      max: 10
    },
    migrations: {
      tableName: 'knex_migrations'
    }
  }
};
