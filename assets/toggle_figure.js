window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        testFunction: function(checkedBoxes, options) {
            if(options.length == 0) {
                return 'test'
            }

            optionsString = options[0].map(option => option.value)

            let toHide = optionsString.filter(x => !checkedBoxes[0].includes(x)).map( id => `.figure-${id}` )
            let toShow = optionsString.filter(x => checkedBoxes[0].includes(x)).map( id => `.figure-${id}` )
            $(toShow.join(',')).show()
            $(toHide.join(',')).hide()
            return 'test'
        }
    }
});
