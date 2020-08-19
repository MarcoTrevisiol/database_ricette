(function() {
    'use strict';
    
    angular
        .module('recipes')
        .controller('SelectRecipeController', SelectRecipeController);

    SelectRecipeController.$inject = ['ApiRicetteFactory', 'RicettaFactory', '$log'];

    
    function SelectRecipeController(ApiRicetteFactory, RicettaFactory, $log) {
        var vm = this;
        vm.titoli = [];
        vm.ricettaHandle = RicettaFactory;
        vm.propertyKey = titoloKey;
        vm.reverse = false;
        vm.sortBy = sortBy;
        vm.properComparator = properComparator;
        vm.titoloKey = titoloKey;
        vm.fonteKey = fonteKey;
        vm.categorieKey = categorieKey;
        vm.tempoKey = tempoKey;
        vm.portataKey = portataKey;
        
        activate();
        
        
        function activate() {
            ApiRicetteFactory.GetListaRicette().then(function (answer) {
                vm.titoli = answer.data;
                $log.log(answer.data);
            });
        }
        
        function sortBy (propertyKey) {
            if (vm.propertyKey[0] === propertyKey) {
                vm.reverse = !vm.reverse;
            }
            else {
                vm.reverse = false;
            }
            vm.propertyKey = [propertyKey, titoloKey];
        }
        
        function properComparator(v1, v2) {
            if (vm.propertyKey == 'categorie') {
                
                return (v1[vm.propertyKey][0].toLowerCase() < v2[vm.propertyKey][0].toLowerCase()) ? -1 : 1;
            }
            if (vm.propertyKey == 'tempo') {
                console.log('qua');
                return (moment.duration(v1[vm.propertyKey]).asSeconds() < moment.duration(v2[vm.propertyKey]).asSeconds()) ? -1 : 1;
            }
            return (v1[vm.propertyKey] < v2[vm.propertyKey]) ? -1 : 1;
        }
        
        function titoloKey(v) {
            return v['titolo'].toLowerCase();
        }
        
        function fonteKey(v) {
            return v['fonte'].toLowerCase();
        }
        
        function categorieKey(v) {
            var item = v['categorie'];
            if (item.length > 0) {
                return item[0].toLowerCase();
            }
            return '';
        }
        
        function tempoKey(v) {
            return moment.duration(v['tempo']).asMinutes();
        }
        
        function portataKey(v) {
            return v['portata'];
        }
    }
})();
