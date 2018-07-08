var app = new Vue({
    el: '#vue_app',
    data: {
        formheight: "auto",
        service : active_logger,
    },
    methods:{
        ani_start: function(){
            var style = this.$refs.vform.currentStyle || window.getComputedStyle(this.$refs.vform);
            var margintop = parseInt(style.marginTop.slice(0,-2));
            var marginbottom = parseInt(style.marginBottom.slice(0,-2));
            this.formheight = this.$refs.vform.offsetHeight + margintop + marginbottom + "px";
        },
        ani_end: function(){
            this.formheight = "auto";
        }
    },
    updated:function(){
        if(this.formheight != 'auto'){
            this.ani_start();
        }
    }
    
})