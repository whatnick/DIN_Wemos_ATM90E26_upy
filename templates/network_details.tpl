<div
    ref="acc_{{ network.id }}" 
    :style="accStyles({{ network.id }})"
    :class="accClasses({{ network.id }})"
>
    <form 
        v-cloak 
        class="form form__network"
        method="post"
    >
        <p><label>Password <input name="pwd" id="pwd" type="password" value="{{ network.pwd }}"></label></p>
        <p>
        
        <input name="ssid" id="ssid" type="hidden" value="{{ network.ssid }}">
        
        {% if network.pwd or network.connected %}
            <button name="forget" type="submit" class="button button--inv">Forget</button> 
        {% endif %}
        
        {% if not network.connected %}
            <button name="connect" type="submit" class="button--inv">Connect</button>
        {% endif %}
        </p>
    </form>
</div>