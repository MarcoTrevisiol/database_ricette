angular
    .module('recipes')
    .factory('ModelliFactory', ModelliFactory)

function ModelliFactory() {
    var modelli = {
        'ingrediente': function () {
            this.nome = '';
            this.principale = false;
            this.quantita = {'valore': '', 'unita': ''};
        },
        'variante': function () {
            this.ingredienti = [];
            this.procedura = '';
        }
    };
    modelli['parte'] = function () {
        this.nome = 'parte secondaria';
        this.ingredienti = [new modelli['ingrediente']()];
        this.procedura = '';
        this.varianti = [];
    };
    modelli['partePrincipale'] = function () {
        this.nome = 'parte principale';
        this.ingredienti = [
            new modelli['ingrediente'](),
        ];
        this.procedura = '';
        this.varianti = [];
    };
    return {
        Modello: function (modello) {
            return new modelli[modello]();
        },
    };
};
