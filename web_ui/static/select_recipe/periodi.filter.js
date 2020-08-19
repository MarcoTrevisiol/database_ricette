(function() {
    'use strict';
    
    angular
        .module('recipes')
        .filter('PeriodoFilter', PeriodoFilter);

    
    function PeriodoFilter() {
        return function(isoDuration) {
            var period = moment.duration(isoDuration);
            if (period.asDays() >= 1) {
                return moment.utc(period.asMilliseconds()).format("D[d] h[h] m[m]");
            }
            if (period.asHours() >= 1) {
                return moment.utc(period.asMilliseconds()).format("h[h] m[m]");
            }
            return moment.utc(period.asMilliseconds()).format("m[m]")
        };
    }
})();
