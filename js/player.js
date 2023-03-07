
videojs.Hls.xhr.beforeRequest = function (options) {

    let newUri = options.uri.includes('.ts') ? options.uri + "?q=test" : options.uri;

    return {
        ...options,
        uri: newUri
    };

};



let player = videojs("my-video", { responsive: true }, () => {
    console.log("Start");


    player.one("loadedmetadata", () => {

        let qualities = player.
            tech({ IWillNotUseThisInPlugins: true }).
            hls.representations();
        console.log('qualities', qualities);
        createButtonsQualities({
            class: "item",
            qualities: qualities,
            father: player.controlBar.el_
        });


        player.play();

        function createAutoQualityButton(params) {
            let button = document.createElement("div");

            button.id = "auto";
            button.innerText = `Auto`;

            button.classList.add("selected");

            if (params && params.class) button.classList.add(params.class);

            button.addEventListener("click", () => {
                removeSelected(params);
                button.classList.add("selected");
                qualities.map(quality => quality.enabled(true));
            });

            return button;
        }

        function createButtonsQualities(params) {

            let contentMenu = document.createElement('div');
            let menu = document.createElement('div');
            let icon = document.createElement('div');

            let fullscreen = params.father.querySelector('.vjs-fullscreen-control');
            contentMenu.appendChild(icon);
            contentMenu.appendChild(menu);
            fullscreen.before(contentMenu);

            menu.classList.add('menu');
            icon.classList.add('icon', 'vjs-icon-cog');
            contentMenu.classList.add('contentMenu');

            let autoButton = createAutoQualityButton(params);

            menu.appendChild(autoButton);

            qualities.sort((a, b) => {
                return a.height > b.height ? 1 : 0;
            });

            qualities.map(quality => {
                let button = document.createElement("div");

                if (params && params.class) button.classList.add(params.class);

                button.id = `${quality.height}`;
                button.innerText = quality.height + "p";

                button.addEventListener("click", () => {
                    resetQuality(params);
                    button.classList.add("selected");
                    quality.enabled(true);
                });

                menu.appendChild(button);
            });

            setInterval(() => {
                let auto = document.querySelector("#auto");
                current = player.
                    tech({ IWillNotUseThisInPlugins: true }).
                    hls.selectPlaylist().attributes.RESOLUTION.height;
                console.log(current);

                document.querySelector("#auto").innerHTML = auto.classList.contains(
                    "selected") ?

                    `Auto <span class='current'>${current}p</span>` :
                    "Auto";
            }, 1000);


        }

        function removeSelected(params) {
            document.querySelector("#auto").classList.remove("selected");
            [...document.querySelectorAll(`.${params.class}`)].map(quality => {
                quality.classList.remove("selected");
            });
        }

        function resetQuality(params) {
            removeSelected(params);

            for (let quality of params.qualities) {
                quality.enabled(false);
            }
        }
    });
});
