window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        testFunction: function(checkedBoxes, options) {
            for (let i = 0; i < options.length; i++) {
                if(options[i].length === 0) {
                    continue
                }

                optionsString = options[i].map(option => option.value)

                let toHide = optionsString.filter(x =>
                    !checkedBoxes[i].includes(x)).map( id => `.figure-${id}`
                    )

                let toShow = optionsString.filter(
                    x => checkedBoxes[i].includes(x)).map( id => `.figure-${id}`
                    )

                $(toShow.join(',')).show()
                $(toHide.join(',')).hide()
            }
        }
    }
});
