function getQueue(seed) {
    var queue = []
    var alea = require('alea')

    var blockRNG=new alea(seed);                 // seed the randomizer
    var bag=["I","O","T","L","J","S","Z"];   // block indices
    function getBlock(){
        var index = Math.floor(blockRNG() * bag.length);     // random index in the current bag
        var rand = bag.splice(index,1)[0];                   // get the block an  d remove from the current bag
        if(bag.length === 0) bag = ["I","O","T","L","J","S","Z"];         // refreshes the bag to the original state (above)
        return rand;
    }
    for(var i=0;i<110;i++) {
        queue.push(getBlock())
    }
    return queue
}