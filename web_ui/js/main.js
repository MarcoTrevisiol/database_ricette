function ModelliFactory() {
    var modelli = {
        'ingrediente': function () {
            this.nome = '';
            this.principale = false;
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
            {
                'nome': '',
                'principale': true,
            },
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

function ApiRicetteFactory($http) {
    var url_nuova_ricetta = '/cgi-bin/main.py/nuova_ricetta';
    return {
        PostRicetta: function (ricetta) {
            return $http.post(url_nuova_ricetta, ricetta);
        },
        GetPortate: function () {
            return {
                'Primo': 'images/Primo.jpg',
                'Secondo': 'images/Secondo.jpg',
                'Contorno': 'images/Contorno.jpg',
                'Dolce': 'images/Dolce.jpg',
            };
        },
        GetPeriodi: function () {
            return {
                'Primavera': ['mar', 'apr', 'mag'],
                'Estate': ['giu', 'lug', 'ago'],
                'Autunno': ['set', 'ott', 'nov'],
                'Inverno': ['dic', 'gen', 'feb'],
                'Tutti': ['gen', 'feb', 'mar', 'apr', 'mag', 'giu', 'lug', 'ago', 'set', 'ott', 'nov', 'dic'],
                'Niente': [],
            };
        },
    };
};

function Controller(ModelliFactory, ApiRicetteFactory, $sce, $log) {
    var vm = this;
    vm.ricetta = {};
    vm.ricetta.titolo = "Titolo della ricetta";
    vm.fotoPortate = ApiRicetteFactory.GetPortate();
    vm.portate = Object.keys(vm.fotoPortate);
    vm.ricetta.portata = vm.portate[0];
    
    vm.ricetta.tempo = 'PT30M';
    
    vm.periodi = ApiRicetteFactory.GetPeriodi();
    vm.nomiPeriodi = Object.keys(vm.periodi);
    vm.categorie = '';
    vm.mesi = vm.periodi['Tutti'];
    
    vm.mesiSelezionati = {}
    for (m in vm.mesi) {
        vm.mesiSelezionati[vm.mesi[m]] = true;
    }
    $log.log(vm.mesiSelezionati);
    
    vm.SetMesi = function (periodo) {
        $log.log(periodo);
        if ( !(periodo in vm.periodi) )
            periodo = 'Tutti';
        for (m in vm.mesi) {
            var daAggiungere = vm.periodi[periodo].includes(vm.mesi[m]);
            $log.log(vm.mesi[m], daAggiungere);
            vm.mesiSelezionati[vm.mesi[m]] = daAggiungere;
        }
    };
    
    vm.ricetta.parti = [ModelliFactory.Modello('partePrincipale')];
    
    vm.Togli = function (contenitore, ingrediente) {
        var index = contenitore.indexOf(ingrediente);
        if (index > -1) {
            contenitore.splice(index, 1);
        }
    };
    vm.Aggiungi = function (contenitore, modello) {
        contenitore.push(ModelliFactory.Modello(modello));
    };

    vm.MandaRichiesta = function () {
        vm.ricetta['periodo'] = [];
        for (m in vm.mesi) {
            if (vm.mesiSelezionati[vm.mesi[m]])
                vm.ricetta['periodo'].push(vm.mesi[m]);
        }
        vm.ricetta['categorie'] = vm.categorie.split(/[,;.:]/).filter(value => value != '');
        
        $log.log(vm.ricetta);
        ApiRicetteFactory.PostRicetta(vm.ricetta)
            .then(function (response) {
                vm.posto = {
                    status: response.status,
                    data: $sce.trustAsHtml(response.data),
                }
            });
    };
};

function RecDurationDirective() {
    return {
        restrict: 'A',
        require: 'ngModel',
        link: function(scope, element, attr, ngModelCtrl) {
            function fromUser(minuti) {
                return moment.duration(minuti, 'minutes').toISOString();
            }

            function toUser(isoString) {
                return moment.duration(isoString).asMinutes();
            }
            ngModelCtrl.$parsers.push(fromUser);
            ngModelCtrl.$formatters.push(toUser);
        },
    };
};


function contenteditable() {
    return {
        require: 'ngModel',
        link: function(scope, element, attr, ngModelCtrl) {
            // view -> model
            element.on('blur', function() {
                ngModelCtrl.$setViewValue(element.html());
            });

            // model -> view
            ngModelCtrl.$render = function() {
                element.html(ngModelCtrl.$viewValue);
            };

            // load init value from DOM
            ngModelCtrl.$render;
        }
    };
};

angular
    .module('recipes', [])
    .factory('ModelliFactory', ModelliFactory)
    .factory('ApiRicetteFactory', ['$http', ApiRicetteFactory])
    .directive('recDuration', RecDurationDirective)
    .directive('contenteditable', contenteditable)
    .controller('Controller', ['ModelliFactory', 'ApiRicetteFactory', '$sce', '$log', Controller]);
