<div
    ref="acc_{{ key }}" 
    :style="accStyles({{ key }})"
    :class="accClasses({{ key }})"
>
    <form 
        v-cloak 
        class="form form__network"
        method="post"
    >
        <p><label>Password <input name="pwd" id="pwd" type="password" value="{{ network.pwd }}"></label></p>
        <p>
        
        <input name="ssid" id="ssid" type="hidden" value="{{ network.ssid }}">
        
        {% if network.pwd or  network.ssid == connected_network %}
            <button name="forget" type="submit" class="button button--inv">Forget</button> 
        {% endif %}
        
        {% if  network.ssid != connected_network %}
            <button name="connect" type="submit" class="button--inv">Connect</button>
        {% endif %}
        </p>
    </form>
</div>