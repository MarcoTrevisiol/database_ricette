(function() {
    'use strict';
    
    angular
        .module('recipes')
        .factory('RicettaFactory', RicettaFactory);

    function RicettaFactory() {
        return {
            dosi: 4,
            titolo: "Titolo della ricetta",
            tempo: 'PT30M',
        };
    };
})();
