(function() {
    'use strict';

    angular
        .module('recipes')
        .factory('ModelliFactory', ModelliFactory);

        
    function ModelliFactory() {
        var modelli = {
            'ingrediente': Ingrediente,
            'variante': Variante,
            'parte': Parte,
            'partePrincipale': PartePrincipale,
        };
        var service = {
            Modello: function (modello) {
                return new modelli[modello]();
            },
        };
        
        return service;
        
        
        function Ingrediente () {
            this.nome = '';
            this.principale = false;
            this.quantita = {'valore': '', 'unita': ''};
        }
        
        function Variante() {
                this.ingredienti = [];
                this.procedura = '';
        }
        
        function Parte() {
            this.nome = 'parte secondaria';
            this.ingredienti = [new modelli['ingrediente']()];
            this.procedura = '';
            this.varianti = [];
        }
        
        function PartePrincipale() {
            this.nome = 'parte principale';
            this.ingredienti = [
                new modelli['ingrediente'](),
            ];
            this.procedura = '';
            this.varianti = [];
        }
    };
})();
