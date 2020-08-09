(function() {
    'use strict';

    angular
        .module('recipes')
        .factory('ModelliFactory', ModelliFactory);

        
    function ModelliFactory() {
        var modelli = {
            'ingrediente': ingrediente,
            'variante': variante,
            'parte': parte,
            'partePrincipale': partePrincipale,
        };
        var service = {
            Modello: function (modello) {
                return new modelli[modello]();
            },
        };
        
        return service;
        
        
        function ingrediente () {
            this.nome = '';
            this.principale = false;
            this.quantita = {'valore': '', 'unita': ''};
        };
        
        function variante() {
                this.ingredienti = [];
                this.procedura = '';
        };
        
        function parte() {
            this.nome = 'parte secondaria';
            this.ingredienti = [new modelli['ingrediente']()];
            this.procedura = '';
            this.varianti = [];
        };
        
        function partePrincipale() {
            this.nome = 'parte principale';
            this.ingredienti = [
                new modelli['ingrediente'](),
            ];
            this.procedura = '';
            this.varianti = [];
        };
    };
})();
