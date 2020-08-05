function ModelliFactory() {
    var modelli = {
        'ingrediente': function () {
            this.nome = 'a';
            this.principale = false;
            this.quantita = {'valore': 1, 'unita': ' u'};
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
                'nome': 'b',
                'principale': true,
                'quantita': {'valore': 1, 'unita': ' u'},
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

function NormalizzaDosiFactory() {
    return {
        Normalizza: function (ricetta, dosi) {
            for (p in ricetta.parti) {
                parte = ricetta.parti[p];
                for (i in parte.ingredienti) {
                    ingrediente = parte.ingredienti[i];
                    ingrediente.quantita.valore /= dosi;
                }
                for (v in parte.varianti) {
                    for (i in parte.varianti[v].ingredienti) {
                        ingrediente = parte.varianti[v].ingredienti[i];
                        ingrediente.quantita.valore /= dosi;
                    }
                }
            }
        },
    };
};

function Controller(ModelliFactory, ApiRicetteFactory, NormalizzaDosiFactory, $timeout, $log) {
    var vm = this;
    vm.ricetta = {};
    vm.ricetta.titolo = "Titolo della ricetta";
    vm.dosi = 4;
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
    
    vm.Togli = function (contenitore, oggetto) {
        var index = contenitore.indexOf(oggetto);
        if (index > -1) {
            contenitore.splice(index, 1);
        }
    };
    vm.Aggiungi = function (contenitore, modello) {
        contenitore.push(ModelliFactory.Modello(modello));
    };
    
    vm.Muovi = function (contenitore, oggetto, direzione) {
        var index = contenitore.indexOf(oggetto);
        if (index > -1) {
            $log.log(contenitore, oggetto, direzione, index);
            if (index == 0 && direzione == -1)
                return;
            if (index == contenitore.length-1 && direzione == 1)
                return;
            contenitore.splice(index, 1);
            contenitore.splice(index + direzione, 0, oggetto);
        }
    };
    
    vm.EPrimo = function (contenitore, oggetto) {
        return contenitore.indexOf(oggetto) == 0;
    };
    vm.EUltimo = function (contenitore, oggetto) {
        return contenitore.indexOf(oggetto) == contenitore.length-1;
    };
    
    vm.MandaRichiesta = function () {
        vm.ricetta['periodo'] = [];
        for (m in vm.mesi) {
            if (vm.mesiSelezionati[vm.mesi[m]])
                vm.ricetta['periodo'].push(vm.mesi[m]);
        }
        vm.ricetta['categorie'] = vm.categorie.split(/[,;.:]/).filter(value => value != '');
        
        NormalizzaDosiFactory.Normalizza(vm.ricetta, vm.dosi);
        $log.log(vm.ricetta);
        ApiRicetteFactory.PostRicetta(vm.ricetta)
            .then(function (response) {
                NormalizzaDosiFactory.Normalizza(vm.ricetta, 1/vm.dosi);
                vm.posto = {
                    status: response.status,
                    codice: response.data.codice,
                    messaggio: response.data.messaggio,
                }
                $timeout(function () { vm.posto.status = 0; }, 10000);
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

            // load init value from Model
            ngModelCtrl.$render();
        }
    };
};

function RecQuantitaDirective() {
    return {
        restrict: 'A',
        require: 'ngModel',
        link: function(scope, element, attr, ngModelCtrl) {
            function fromUser(quanto) {
                number = quanto.match(/^[0-9]*(.[0-9]*)?/)[0];
                unitRegex = number + "\(.*\)$";
                unit = quanto.match(unitRegex)[1];
                if (number.length > 0)
                    amount = parseFloat(number);
                else
                    amount = 1;
                return {
                    valore: amount,
                    unita: unit,
                };
            }

            function toUser(quanto) {
                return quanto.valore.toString() + quanto.unita;
            }
            ngModelCtrl.$parsers.push(fromUser);
            ngModelCtrl.$formatters.push(toUser);
        },
    };
};


angular
    .module('recipes', [])
    .factory('ModelliFactory', ModelliFactory)
    .factory('ApiRicetteFactory', ['$http', ApiRicetteFactory])
    .factory('NormalizzaDosiFactory', NormalizzaDosiFactory)
    .directive('recDuration', RecDurationDirective)
    .directive('contenteditable', contenteditable)
    .directive('recQuantita', RecQuantitaDirective)
    .controller('Controller', ['ModelliFactory', 'ApiRicetteFactory', 'NormalizzaDosiFactory', '$timeout', '$log', Controller]);
