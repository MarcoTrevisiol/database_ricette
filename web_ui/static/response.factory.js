(function() {
    'use strict';

    angular
        .module('recipes')
        .factory('ResponseFactory', ModelliFactory);

        
    function ModelliFactory() {
        var service = {
            status: 0,
            codice: 'ok',
            messaggio: '',
        };
        
        return service;
    }
})();
