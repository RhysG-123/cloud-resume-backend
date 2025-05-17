const { app } = require('@azure/functions');

app.http('VisitorCounter', {
    methods: ['GET'],
    authLevel: 'anonymous',
    handler: require('./functions/VisitorCounter')
});
