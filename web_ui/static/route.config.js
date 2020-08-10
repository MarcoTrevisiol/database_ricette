(function() {
    'use strict';
    
    angular
        .module('recipes')
        .config(configRoute);
    
    configRoute.$inject = ['$routeProvider'];
    
    function configRoute($routeProvider) {
        $routeProvider
            .when('/nuova_ricetta', {
                templateUrl: 'static/new_recipe/new_recipe.html',
                controller: 'NewRecipeController',
                controllerAs: 'vm',
            })
            .when('/seleziona_ricetta', {
                templateUrl: 'static/select_recipe/select_recipe.html',
                controller: 'SelectRecipeController',
                controllerAs: 'vm',
            })
            .when('/modifica_ricetta/:ricettaId', {
                templateUrl: 'static/edit_recipe/edit_recipe.html',
                controller: 'EditRecipeController',
                controllerAs: 'vm',
                resolve: {
                    ricettaPrepService: ricettaPrepService
                },
            })
            .otherwise('/nuova_ricetta');
    }
    
    
    function ricettaPrepService($route, ApiRicetteFactory) {
        return ApiRicetteFactory.GetRicetta($route.current.params.ricettaId.substr(1));
    }
})();
