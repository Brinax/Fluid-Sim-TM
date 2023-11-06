/*
 * Gray-Scott
 *
 * A solver of the Gray-Scott model of reaction diffusion.
 *
 * ©2012 pmneila.
 * p.mneila at upm.es
 */

DIFFUSIONPRECISION = 20;
PRESSIONPRECISION = 50;

(function(){
// Canvas.
var canvas;
var canvasQ;
var canvasWidth;
var canvasHeight;

var mMouseX, mMouseY;
var mMouseDown = false;

var mRenderer;
var mScene;
var mCamera;
var mUniforms;
var mColors;
var mColorsNeedUpdate = true;
var mLastTime = 0;

var mVelocity_and_DensityTexture1, mVelocity_and_DensityTexture2;
var mGSMaterial, mScreenMaterial;
var mScreenQuad;

var mVDToggled = false;
var mDPToggled = false;

var mMinusOnes = new THREE.Vector2(-1, -1);

// Some presets.
var presets = [
    { // Default
        //feed: 0.018,
        //kill: 0.051
        feed: 0.037,
        kill: 0.06
    },
    { // Solitons
        feed: 0.03,
        kill: 0.062
    },
    { // Pulsating solitons
        feed: 0.025,
        kill: 0.06
    },
    { // Worms.
        feed: 0.078,
        kill: 0.061
    },
    { // Mazes
        feed: 0.029,
        kill: 0.057
    },
    { // Holes
        feed: 0.039,
        kill: 0.058
    },
    { // Chaos
        feed: 0.026,
        kill: 0.051
    },
    { // Chaos and holes (by clem)
        feed: 0.034,
        kill: 0.056
    },
    { // Moving spots.
        feed: 0.014,
        kill: 0.054
    },
    { // Spots and loops.
        feed: 0.018,
        kill: 0.051
    },
    { // Waves
        feed: 0.014,
        kill: 0.045
    },
    { // The U-Skate World
        feed: 0.062,
        kill: 0.06093
    }
];

// Configuration.
var feed = presets[0].feed;
var kill = presets[0].kill;

init = function()
{
    init_controls();

    canvasQ = $('#myCanvas');
    canvas = canvasQ.get(0);

    canvas.onmousedown = onMouseDown;
    canvas.onmouseup = onMouseUp;
    canvas.onmousemove = onMouseMove;

    mRenderer = new THREE.WebGLRenderer({canvas: canvas, preserveDrawingBuffer: true});

    mScene = new THREE.Scene();
    mCamera = new THREE.OrthographicCamera(-0.5, 0.5, 0.5, -0.5, -10000, 10000);
    mCamera.position.z = 100;
    mScene.add(mCamera);

    mUniforms = {
        screenWidth: {type: "f", value: undefined},
        screenHeight: {type: "f", value: undefined},
        velocity_and_density: {type: "t", value: undefined},
        divergence_and_pression:{type: "t",value:undefined},
        delta: {type: "f", value: 0.0},
        top: {type: "v4", value: new THREE.Vector4(5,0,0,0)},
        bottom: {type: "v4", value: new THREE.Vector4(-5,0,0,0)},
        feed: {type: "f", value: feed},
        kill: {type: "f", value: kill},
        viscosity: {type: "f", value: 0.005},
        densityDiffusion: {type: "f", value: 0.0},
        brush: {type: "v2", value: new THREE.Vector2(-10, -10)},
        color1: {type: "v4", value: new THREE.Vector4(0, 0, 0.0, 0)},
        color2: {type: "v4", value: new THREE.Vector4(0, 1, 0, 0.2)},
        color3: {type: "v4", value: new THREE.Vector4(1, 1, 0, 0.21)},
        color4: {type: "v4", value: new THREE.Vector4(1, 0, 0, 0.4)},
        color5: {type: "v4", value: new THREE.Vector4(1, 1, 1, 0.6)},
        color6: {type: "v4", value: new THREE.Vector4(1, 0, 1, 0.6)}
    };
    mColors = [mUniforms.color1, mUniforms.color2, mUniforms.color3, mUniforms.color4, mUniforms.color5,mUniforms.color6];
    $("#gradient").gradient("setUpdateCallback", onUpdatedColor);

    mDiffusionMaterial = new THREE.ShaderMaterial({
        uniforms: mUniforms,
        vertexShader: document.getElementById('standardVertexShader').textContent,
        fragmentShader: document.getElementById('diffusionFragmentShader').textContent,
    });
    mAdvectionMaterial = new THREE.ShaderMaterial({
            uniforms: mUniforms,
            vertexShader: document.getElementById('standardVertexShader').textContent,
            fragmentShader: document.getElementById('advectionFragmentShader').textContent,
    });
    mDivergenceMaterial = new THREE.ShaderMaterial({
            uniforms: mUniforms,
            vertexShader: document.getElementById('standardVertexShader').textContent,
            fragmentShader: document.getElementById('divergenceFragmentShader').textContent,
    });
    mPressionMaterial = new THREE.ShaderMaterial({
            uniforms: mUniforms,
            vertexShader: document.getElementById('standardVertexShader').textContent,
            fragmentShader: document.getElementById('pressionFragmentShader').textContent,
    });
    mApplyPressionMaterial = new THREE.ShaderMaterial({
            uniforms: mUniforms,
            vertexShader: document.getElementById('standardVertexShader').textContent,
            fragmentShader: document.getElementById('applyPressionFragmentShader').textContent,
    });
    mScreenMaterial = new THREE.ShaderMaterial({
                uniforms: mUniforms,
                vertexShader: document.getElementById('standardVertexShader').textContent,
                fragmentShader: document.getElementById('screenFragmentShader').textContent,
    });

    var plane = new THREE.PlaneGeometry(1.0, 1.0);
    mScreenQuad = new THREE.Mesh(plane, mScreenMaterial);
    mScene.add(mScreenQuad);

    mColorsNeedUpdate = true;

    resize(canvas.clientWidth, canvas.clientHeight);

    render(0);
    mUniforms.brush.value = new THREE.Vector2(0.5, 0.5);
    mLastTime = new Date().getTime();
    requestAnimationFrame(render);
}

function nearestPowerOfTwo(value) {
    return Math.pow(2, Math.round(Math.log(value) / Math.log(2)));
}


var resize = function(width, height,ratio=0.5)
{
    width=nearestPowerOfTwo(width);
    height=nearestPowerOfTwo(height);
    console.log(width);
    console.log(height);
    // Set the new shape of canvas.
    canvasQ.width(width);
    canvasQ.height(height);

    // Get the real size of canvas.
    canvasWidth = canvasQ.width();
    canvasHeight = canvasQ.height();

    mRenderer.setSize(canvasWidth, canvasHeight);

    /*
    /!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\MODIFIED CONTENT /!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\
    */
    var width = canvasWidth*ratio;
    var height = canvasHeight*ratio;
    var data = new Float32Array(width * height * 4);  // 4 car RGBA
    var bandwidth = 0.05 * height

    for (var i = 0; i < height; i++) {
        for (var j = 0; j < width; j++) {
            var index = (i * width + j) * 4;  // Index dans le tableau data

            /*
            // Vitesse
            if (i < height / 2) {
                data[index] = 1.0;     // R pour vitesse en x
                data[index + 1] = Math.random()/20; // G pour vitesse en y
            } else {
                data[index] = -1.0;
                data[index + 1] = Math.random()/20;
            }*/

            // Vitesse
            if (i<height/2) {
                data[index] = 5;  
                
            } else {
                data[index] = -5;
            }

            if(i==0||i==height-1)
            {
                data[index + 1] = 0;
            }
            if(j<width*5.1/10 && j>width*4.9/10&&i<height*5.1/10&&i>height*4.9/10)
                {
                    data[index + 1] = 50
                }
                else
                {
                    data[index + 1] = 0;
                }

            // Double Band
            /*
            if (i > (height / 2 - bandwidth) && i < (height / 2 + bandwidth)||i > ( height-bandwidth)||i < ( bandwidth)) {
                data[index + 2] = 1.0; // B pour densité
            }else {
                data[index + 2] = 0.0;
            }*/
            //Single Band
            /*
            if (i<height/2) {
                data[index + 2] = 1.0; // G pour vitesse en y
            } else {
                data[index + 2] = 0.0;
            }*/
            data[index + 2]= i/height
            if(j<width*5.1/10 && j>width*4.9/10 && (i>height*9/10 ||i<height*1/10))
            {
                if(i>0&&i<height-1)
                {
                    data[index + 2] = 1-i/height
                }
            }



            data[index + 3] = 1.0; 
        }
    }

    var dataTexture = new THREE.DataTexture(data, width, height, THREE.RGBAFormat, THREE.FloatType);
    dataTexture.needsUpdate = true;  // Important pour dire à Three.js de mettre à jour la texture






    mVelocity_and_DensityTexture1 = new THREE.WebGLRenderTarget(width, height, {
        minFilter: THREE.LinearFilter,
        magFilter: THREE.LinearFilter,
        format: THREE.RGBAFormat,
        type: THREE.FloatType,
        wrapS:THREE.RepeatWrapping,
        wrapT:THREE.ClampToEdgeWrapping,
    });



    // Render the data texture to mVelocity_and_DensityTexture1
    var initMaterial = new THREE.MeshBasicMaterial({ map: dataTexture });
    var initPlane = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), initMaterial);
    var initScene = new THREE.Scene();
    initScene.add(initPlane);

    mRenderer.render(initScene, mCamera, mVelocity_and_DensityTexture1);


    /*
    /!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\MODIFIED CONTENT /!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\
    */

    mVelocity_and_DensityTexture2 = new THREE.WebGLRenderTarget(width, height,
                        {minFilter: THREE.LinearFilter,
                         magFilter: THREE.LinearFilter,
                         format: THREE.RGBAFormat,
                         type: THREE.FloatType,
                         wrapS:THREE.RepeatWrapping,
                         wrapT:THREE.ClampToEdgeWrapping
                        });

    mDivergence_and_PressionTexture1=new THREE.WebGLRenderTarget(width, height,
    {minFilter: THREE.LinearFilter,
     magFilter: THREE.LinearFilter,
     format: THREE.RGBAFormat,
     type: THREE.FloatType,
     wrapS:THREE.RepeatWrapping,
     wrapT:THREE.ClampToEdgeWrapping
    });

    mDivergence_and_PressionTexture2=new THREE.WebGLRenderTarget(width, height,
    {minFilter: THREE.LinearFilter,
     magFilter: THREE.LinearFilter,
     format: THREE.RGBAFormat,
     type: THREE.FloatType,
     wrapS:THREE.RepeatWrapping,
     wrapT:THREE.ClampToEdgeWrapping
    });

    mDivergence_and_PressionTexture2.wrapS = THREE.RepeatWrapping;
    mDivergence_and_PressionTexture1.wrapS = THREE.RepeatWrapping;
    mVelocity_and_DensityTexture1.wrapS = THREE.RepeatWrapping;
    mVelocity_and_DensityTexture2.wrapS = THREE.RepeatWrapping;

    mDivergence_and_PressionTexture2.wrapT = THREE.ClampToEdgeWrapping;
    mDivergence_and_PressionTexture1.wrapT = THREE.ClampToEdgeWrapping;
    mVelocity_and_DensityTexture1.wrapT = THREE.ClampToEdgeWrapping;
    mVelocity_and_DensityTexture2.wrapT = THREE.ClampToEdgeWrapping;

    
    mUniforms.divergence_and_pression.value = mDivergence_and_PressionTexture1;
    mUniforms.velocity_and_density.value = mVelocity_and_DensityTexture1;

    mUniforms.screenWidth.value = width;
    mUniforms.screenHeight.value = height;

    mVDToggled=false;
    mDPToggled=false;
}

var startTime = performance.now();
var index=0;
var render = function(time)
{
    if(index%100==0)
    {
                // Enregistrez le temps de fin
        var endTime = performance.now();

        // Calculez la différence
        var timeTaken = endTime - startTime;

        console.log("Temps de calcul:", timeTaken, "millisecondes.");
        startTime = performance.now();
    }
    index+=1
    var dt = (time - mLastTime)/500000.0;
    if(dt > 0.8 || dt<=0)
        dt = 0.8;
    mLastTime = time;

    mUniforms.delta.value =0.1;
    mUniforms.feed.value = feed;
    mUniforms.kill.value = kill;

    //il faut l'étape d'advection, diffusion et projection
    if((index%10==0 &&index>1000)||true){

        diffusion();
        projection();
        advection();
        projection();
        if(index/10==200 && false) //doit être pair comme par ex. 200 (sinon le buffer est en écriture)
        {
            saveFrameDataToFile(mRenderer, mVelocity_and_DensityTexture2)
        }
    }



    if(mColorsNeedUpdate)
        updateUniformsColors();

    mScreenQuad.material = mScreenMaterial;
    mRenderer.render(mScene, mCamera);
    requestAnimationFrame(render);
    
}

projection = function()
{

    mScreenQuad.material = mDivergenceMaterial;
    if(!mDPToggled)
    {
        mUniforms.divergence_and_pression.value=mDivergence_and_PressionTexture1;
        mRenderer.render(mScene, mCamera, mDivergence_and_PressionTexture2, true); //automatiquement dans l'uniform adapté, pas besoin de ping-pong puisque la divergence n'influe pas sur elle-même
        mUniforms.divergence_and_pression.value=mDivergence_and_PressionTexture2;
    }else
    {
        mUniforms.divergence_and_pression.value=mDivergence_and_PressionTexture2;
        mRenderer.render(mScene, mCamera, mDivergence_and_PressionTexture1, true); //automatiquement dans l'uniform adapté, pas besoin de ping-pong puisque la divergence n'influe pas sur elle-même
        mUniforms.divergence_and_pression.value=mDivergence_and_PressionTexture1;
    }

    mDPToggled=!mDPToggled;

    mScreenQuad.material = mPressionMaterial;
    for(var i=0; i<PRESSIONPRECISION; ++i)
    {
        if(!mDPToggled)
        {
            mUniforms.divergence_and_pression.value = mDivergence_and_PressionTexture1;
            mRenderer.render(mScene, mCamera, mDivergence_and_PressionTexture2, true);
            mUniforms.divergence_and_pression.value = mDivergence_and_PressionTexture2;
        }
        else
        {
            mUniforms.divergence_and_pression.value = mDivergence_and_PressionTexture2;
            mRenderer.render(mScene, mCamera, mDivergence_and_PressionTexture1, true);
            mUniforms.divergence_and_pression.value = mDivergence_and_PressionTexture1;
        }

        mDPToggled = !mDPToggled;
        mUniforms.brush.value = mMinusOnes;
    }

    mScreenQuad.material = mApplyPressionMaterial;
    if(!mVDToggled)
    {
        mUniforms.velocity_and_density.value=mVelocity_and_DensityTexture1;
        mRenderer.render(mScene, mCamera, mVelocity_and_DensityTexture2, true);
        mUniforms.velocity_and_density.value=mVelocity_and_DensityTexture2;
    }else
    {
        mUniforms.velocity_and_density.value=mVelocity_and_DensityTexture2;
        mRenderer.render(mScene, mCamera, mVelocity_and_DensityTexture1, true);
        mUniforms.velocity_and_density.value=mVelocity_and_DensityTexture1;
    }
    mVDToggled=!mVDToggled;
}

diffusion = function()
{

    mScreenQuad.material = mDiffusionMaterial;
    for(var i=0; i<DIFFUSIONPRECISION; ++i)
    {
        if(!mVDToggled)
        {
            mUniforms.velocity_and_density.value = mVelocity_and_DensityTexture1;
            mRenderer.render(mScene, mCamera, mVelocity_and_DensityTexture2, true);
            mUniforms.velocity_and_density.value = mVelocity_and_DensityTexture2;
        }
        else
        {
            mUniforms.velocity_and_density.value = mVelocity_and_DensityTexture2;
            mRenderer.render(mScene, mCamera, mVelocity_and_DensityTexture1, true);
            mUniforms.velocity_and_density.value = mVelocity_and_DensityTexture1;
        }

        mVDToggled = !mVDToggled;
        mUniforms.brush.value = mMinusOnes;
    }
}

advection = function()
{
    
    mScreenQuad.material = mAdvectionMaterial;
    if(!mVDToggled)
    {
        mUniforms.velocity_and_density.value=mVelocity_and_DensityTexture1;
        mRenderer.render(mScene, mCamera, mVelocity_and_DensityTexture2, true);
        mUniforms.velocity_and_density.value=mVelocity_and_DensityTexture2;
    }else
    {
        mUniforms.velocity_and_density.value=mVelocity_and_DensityTexture2;
        mRenderer.render(mScene, mCamera, mVelocity_and_DensityTexture1, true);
        mUniforms.velocity_and_density.value=mVelocity_and_DensityTexture1;
    }
    mVDToggled=!mVDToggled;
}
function saveFrameDataToFile(renderer, renderTarget) {
    const gl = renderer.getContext(); // Obtient le contexte WebGL
    const width = renderTarget.width;
    const height = renderTarget.height;

    // Crée un buffer pour lire les pixels
    const pixels = new Float32Array(width * height * 4);

    // Configure le renderer pour utiliser le render target
    renderer.setRenderTarget(renderTarget);

    // Rendu hors écran
    renderer.render(mScene, mCamera);

    // Active le render target pour la lecture
    gl.bindFramebuffer(gl.FRAMEBUFFER, renderTarget.__webglFramebuffer);

    // Lis les données du framebuffer
    gl.readPixels(0, 0, width, height, gl.RGBA, gl.FLOAT, pixels);
    // Convertis les données en chaîne de caractères avec des # comme séparateurs et deux chiffres après la virgule
    let dataString1 = width.toString()+"W"+height.toString()+"H";
    let dataString2 = width.toString()+"W"+height.toString()+"H";
    let dataString3 = width.toString()+"W"+height.toString()+"H";
    for (let i = 0; i < pixels.length; i+=4) {
        const r = pixels[i].toFixed(2);
        const g = pixels[i + 1].toFixed(2);
        const b = pixels[i + 2].toFixed(2);
        const a = pixels[i + 3].toFixed(2);
        
        dataString1 += `${r}`; // Sépare les valeurs par un #
        dataString2 += `${g}`; // Sépare les valeurs par un #
        dataString3 += `${b}`; // Nouvelle ligne pour chaque pixel
        dataString1 += "\\"; // Nouvelle ligne pour chaque pixel
        dataString2 += "\\"; // Nouvelle ligne pour chaque pixel
        dataString3 += "\\";
    }
    downloadStringAsFile(dataString1+"#", 'GPUkelvin-HelmholtzX.txt');
    downloadStringAsFile(dataString2+"#", 'GPUkelvin-HelmholtzY.txt');
    downloadStringAsFile(dataString3+"#", 'GPUkelvin-HelmholtzD.txt');
}
function downloadStringAsFile(dataString, filename) {
    const element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(dataString));
    element.setAttribute('download', filename);

    element.style.display = 'none';
    document.body.appendChild(element);

    // Déclenche le téléchargement
    element.click();

    // Nettoie et supprime l'élément 'a'
    document.body.removeChild(element);
}
loadPreset = function(idx)
{
    feed = presets[idx].feed;
    kill = presets[idx].kill;
    worldToForm();
}

var updateUniformsColors = function()
{
    var values = $("#gradient").gradient("getValuesRGBS");
    for(var i=0; i<values.length; i++)
    {
        var v = values[i];
        mColors[i].value = new THREE.Vector4(v[0], v[1], v[2], v[3]);
    }

    mColorsNeedUpdate = false;
}

var onUpdatedColor = function()
{
    mColorsNeedUpdate = true;
    updateShareString();
}

var onMouseMove = function(e)
{
    var ev = e ? e : window.event;

    mMouseX = ev.pageX - canvasQ.offset().left; // these offsets work with
    mMouseY = ev.pageY - canvasQ.offset().top; //  scrolled documents too

    if(mMouseDown)
        mUniforms.brush.value = new THREE.Vector2(mMouseX/canvasWidth, 1-mMouseY/canvasHeight);
}

var onMouseDown = function(e)
{
    var ev = e ? e : window.event;
    mMouseDown = true;

    mUniforms.brush.value = new THREE.Vector2(mMouseX/canvasWidth, 1-mMouseY/canvasHeight);
}

var onMouseUp = function(e)
{
    mMouseDown = false;
}

clean = function()
{
    mUniforms.brush.value = new THREE.Vector2(-10, -10);
}

downloadURI = function(uri, name)
{
    var link = document.createElement("a");
    link.download = name;
    link.href = uri;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    delete link;
}

snapshot = function()
{
    var dataURL = canvas.toDataURL("image/png");
    downloadURI(dataURL, "grayscott.png");
}

// resize canvas to fullscreen, scroll to upper left
// corner and try to enable fullscreen mode and vice-versa
fullscreen = function() {

    var canv = $('#myCanvas');
    var elem = canv.get(0);

    if(isFullscreen())
    {
        // end fullscreen
        if (elem.cancelFullscreen) {
            elem.cancelFullscreen();
        } else if (document.mozCancelFullScreen) {
            document.mozCancelFullScreen();
        } else if (document.webkitCancelFullScreen) {
            document.webkitCancelFullScreen();
        }
    }

    if(!isFullscreen())
    {
        // save current dimensions as old
        window.oldCanvSize = {
            width : canv.width(),
            height: canv.height()
        };

        // adjust canvas to screen size
        resize(screen.width, screen.height,0.25);

        // scroll to upper left corner
        $('html, body').scrollTop(canv.offset().top);
        $('html, body').scrollLeft(canv.offset().left);

        // request fullscreen in different flavours
        if (elem.requestFullscreen) {
            elem.requestFullscreen();
        } else if (elem.mozRequestFullScreen) {
            elem.mozRequestFullScreen();
        } else if (elem.webkitRequestFullscreen) {
            elem.webkitRequestFullscreen();
        }
    }
}

var isFullscreen = function()
{
    return document.mozFullScreenElement ||
        document.webkitCurrentFullScreenElement ||
        document.fullscreenElement;
}

$(document).bind('webkitfullscreenchange mozfullscreenchange fullscreenchange', function(ev) {
    // restore old canvas size
    if(!isFullscreen())
        resize(window.oldCanvSize.width, window.oldCanvSize.height);
});

var worldToForm = function()
{
    //document.ex.sldReplenishment.value = feed * 1000;
    $("#sld_replenishment").slider("value", feed);
    $("#sld_diminishment").slider("value", kill);
}

var init_controls = function()
{
    $("#sld_replenishment").slider({
        value: feed, min: 0, max:0.1, step:0.001,
        change: function(event, ui) {$("#replenishment").html(ui.value); feed = ui.value; updateShareString();},
        slide: function(event, ui) {$("#replenishment").html(ui.value); feed = ui.value; updateShareString();}
    });
    $("#sld_replenishment").slider("value", feed);
    $("#sld_diminishment").slider({
        value: kill, min: 0, max:0.073, step:0.001,
        change: function(event, ui) {$("#diminishment").html(ui.value); kill = ui.value; updateShareString();},
        slide: function(event, ui) {$("#diminishment").html(ui.value); kill = ui.value; updateShareString();}
    });
    $("#sld_diminishment").slider("value", kill);

    $('#share').keypress(function (e) {
        if (e.which == 13) {
            parseShareString();
            return false;
        }
    });

    $("#btn_clear").button({
        icons : {primary : "ui-icon-document"},
        text : false
    });
    $("#btn_snapshot").button({
        icons : {primary : "ui-icon-image"},
        text : false
    });
    $("#btn_fullscreen").button({
        icons : {primary : "ui-icon-arrow-4-diag"},
        text : false
    });

    $("#notworking").click(function(){
        $("#requirement_dialog").dialog("open");
    });
    $("#requirement_dialog").dialog({
        autoOpen: false
    });
}

alertInvalidShareString = function()
{
    $("#share").val("Invalid string!");
    setTimeout(updateShareString, 1000);
}

parseShareString = function()
{
    var str = $("#share").val();
    var fields = str.split(",");

    if(fields.length != 12)
    {
        alertInvalidShareString();
        return;
    }

    var newFeed = parseFloat(fields[0]);
    var newKill = parseFloat(fields[1]);

    if(isNaN(newFeed) || isNaN(newKill))
    {
        alertInvalidShareString();
        return;
    }

    var newValues = [];
    for(var i=0; i<5; i++)
    {
        var v = [parseFloat(fields[2+2*i]), fields[2+2*i+1]];

        if(isNaN(v[0]))
        {
            alertInvalidShareString();
            return;
        }

        // Check if the string is a valid color.
        if(! /^#[0-9A-F]{6}$/i.test(v[1]))
        {
            alertInvalidShareString();
            return;
        }

        newValues.push(v);
    }

    $("#gradient").gradient("setValues", newValues);
    feed = newFeed;
    kill = newKill;
    worldToForm();
}

updateShareString = function()
{
    var str = "".concat(feed, ",", kill);

    var values = $("#gradient").gradient("getValues");
    for(var i=0; i<values.length; i++)
    {
        var v = values[i];
        str += "".concat(",", v[0], ",", v[1]);
    }
    $("#share").val(str);
}

})();
