{% extends "catalog/base.html" %}

{% block content %}
<div style="text-align: center; padding: 50px;">
    <h1>🛒 Ваша корзина</h1>
    <p style="color: #666; font-size: 1.2em;">В корзине пока пусто.</p>
    <br>
    <a href="{% url 'catalog:home' %}" class="btn btn-primary">Вернуться за покупками</a>
</div>
{% endblock %}