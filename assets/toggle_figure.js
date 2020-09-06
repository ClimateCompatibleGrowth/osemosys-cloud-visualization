window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        testFunction: function(checkedBoxes, options) {
          tabIndices = {
            0: 'all',
            1: 'climate',
            2: 'land',
            3: 'energy',
            4: 'water',
          }
            for (let i = 0; i < options.length; i++) {
                if(options[i].length === 0) {
                    continue
                }

                optionsString = options[i].map(option => option.value)

                let toHide = optionsString.filter(x =>
                    !checkedBoxes[i].includes(x)).map( id => `.figure-set-${id}`
                    )

                let toShow = optionsString.filter(
                    x => checkedBoxes[i].includes(x)).map( id => `.figure-set-${id}`
                    )

                $(`#nav-${tabIndices[i]}`).find(toShow.join(',')).show()
                $(`#nav-${tabIndices[i]}`).find(toHide.join(',')).hide()
            }
        }
    }
});
