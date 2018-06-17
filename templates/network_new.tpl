<div 
    ref="acc_new" 
    :style="accStyles('new')"
    :class="accClasses('new')"
>
    <form 
        v-cloak  
        class="form form__network"
        method="post"
        action="/networks"
    >
        <p><label>Name <input name="ssid" type="text"></label></p>
        <p><label>Password <input name="pwd" type="text"></label></p>
        <p><button name="connect" class="button--inv" type="submit">Connect</button></p>
    </form>
</div>