(function() {
  'use strict';

  angular
    .module('static')
    .controller('MainController', MainController);

  /** @ngInject */
  function MainController(googlePlaces, places, $interval, $mdBottomSheet) {
    var vm = this;
    vm.places = [];
    // Search for places based geo location
    vm.search = function() {
      vm.places = [];
      googlePlaces.getPlaces()
        .then(function(places) {
          vm.spin = !vm.spin;
          return (vm.places = places);
        })
        .then(vm.ratePlaces);
    };
    // rate places
    vm.ratePlaces = function(list) {
      list.forEach(function(p) {
        if (!/^[A-Za-z][A-Za-z0-9 ]*$/.test(p.name.replace('-', ' '))) {
          p.dValue = -1;
          return;
        }
        var stop = $interval(function() {
          p.dValue = (p.dValue || 0) + Math.random();
        }, 300);
        places.ratePlace(p.name.replace(/ /g, '').toLowerCase())
          .then(function(ratePlace) {
            $interval.cancel(stop);
            p.rating = ratePlace.rating;
            p.dValue = 100;
            return p;
          })
          .then(vm.fillPhotos);
      });
    };

    // Fill photos for each place
    vm.fillPhotos = function(pl) {
      var pname = pl.name.replace(/ |-/g, '').toLowerCase();
      places.getPhotos(pname, [pl.geometry.location.G, pl.geometry.location.K].join(','))
        .then(function(ins_details) {
          pl.$photos = ins_details.photos;
          pl.$posts = ins_details.posts;
        });
    };

    vm.alert = '';
    vm.showDialog = function($event, place) {
      vm.alert = '';
      $mdBottomSheet.show({
        templateUrl: 'app/main/bottom-sheet-list-template.html',
        controller: ['$scope', '$mdBottomSheet',function($scope, $mdBottomSheet) {
          $scope.place = place;
          $scope.listItemClick = function($index) {
            var clickedItem = $scope.items[$index];
            $mdBottomSheet.hide(clickedItem);
          };
        }],
        targetEvent: $event
      })
      .then(function(clickedItem) {
        vm.alert = clickedItem.name + ' clicked!';
      });
    };
  }
})();
