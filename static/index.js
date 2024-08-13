function initialize(constraints) {
    // load constraint labels
    for (let i = 0; i < 2; i++) {
        for (let j = 0; j < 3; j++) {
            const tag = "#c" + i.toString() + j.toString();
            const idx = i*3 + j;
            $(tag).text(constraints[idx]);
        }
    }

    // // load autocomplete list for grid inputs
    // for (let i = 0; i < 3; i++) {
    //     for (let j = 0; j < 3; j++) {
    //         const tag = "#t" + i.toString() + j.toString();
    //         $(tag).autocomplete({
    //             source: autocomplete_list
    //         });
    //     }
    // }
}