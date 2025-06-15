from django.db import models
from django.conf import settings
from store.models import Product, Category, Specification
from decimal import Decimal

class PCBuildComponent(models.Model):
    build = models.ForeignKey('PCBuild', on_delete=models.CASCADE, related_name='components')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('build', 'category')
        verbose_name = 'Компонент сборки'
        verbose_name_plural = 'Компоненты сборки'

class PCBuild(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pc_builds')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Можно добавить is_active, если нужно хранить историю

    class Meta:
        verbose_name = 'Сборка ПК'
        verbose_name_plural = 'Сборки ПК'

class SavedPCBuild(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_pc_builds')
    name = models.CharField(max_length=255)
    data = models.JSONField()  # Сохраняем структуру сборки (product_id, category_id, quantity)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Сохраненная сборка'
        verbose_name_plural = 'Сохраненные сборки'

class CompatibilityRule(models.Model):
    OPERATOR_CHOICES = [
        ('=', 'Равно'),
        ('!=', 'Не равно'),
        ('<', 'Меньше'),
        ('<=', 'Меньше или равно'),
        ('>', 'Больше'),
        ('>=', 'Больше или равно'),
    ]
    category1 = models.ForeignKey(Category, verbose_name='Категория 1', on_delete=models.CASCADE, related_name='compat_rules_1')
    spec1 = models.ForeignKey(Specification, verbose_name='Характеристика 1', on_delete=models.CASCADE, related_name='compat_rules_1')
    operator = models.CharField('Оператор', max_length=2, choices=OPERATOR_CHOICES)
    category2 = models.ForeignKey(Category, verbose_name='Категория 2', on_delete=models.CASCADE, related_name='compat_rules_2')
    spec2 = models.ForeignKey(Specification, verbose_name='Характеристика 2', on_delete=models.CASCADE, related_name='compat_rules_2')
    error_message = models.CharField('Сообщение об ошибке', max_length=255)

    class Meta:
        verbose_name = 'Правило совместимости'
        verbose_name_plural = 'Правила совместимости'

    def __str__(self):
        return f'{self.category1} {self.spec1} {self.operator} {self.category2} {self.spec2}'
    

class CategoryPC(models.Model):
    CATEGORY_CHOICES = [
        ('gaming', 'Для игр'),
        ('work', 'Для работы'),
        ('office', 'Для офиса'),
        ('design', 'Для дизайна'),
        ('study', 'Для учебы'),
        ('streaming', 'Для стриминга'),
    ]
    
    name = models.CharField(max_length=50, choices=CATEGORY_CHOICES, unique=True)
    display_name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    icon = models.CharField(max_length=50)  # CSS класс для иконки или путь к изображению
    
    class Meta:
        verbose_name = 'Категория ПК'
        verbose_name_plural = 'Категории ПК'

    def __str__(self):
        return self.display_name

class Computer(models.Model):
    LEVEL_CHOICES = [
        ('start', 'Начальный уровень'),
        ('pro', 'Оптимальный выбор'),
        ('ultra', 'Максимальная мощность'),
    ]
    
    category = models.ForeignKey(CategoryPC, on_delete=models.CASCADE, related_name='computers')
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Характеристики
    processor = models.CharField(max_length=100)
    graphics_card = models.CharField(max_length=100)
    ram = models.CharField(max_length=50)
    storage = models.CharField(max_length=50)
    
    # Цвет для выделения уровня
    level_color = models.CharField(max_length=20, default='blue-500')
    
    class Meta:
        ordering = ['price']
        verbose_name = 'Компьютер'
        verbose_name_plural = 'Компьютеры'
    
    def __str__(self):
        return f"{self.name} - {self.get_level_display()}"
    
    def formatted_price(self):
        return f"{int(self.price):,}".replace(',', ' ') + ' ₽'

# Добавим модели для готовых сборок
class PrebuiltPC(models.Model):
    LEVEL_CHOICES = [
        ('start', 'Начальный уровень'),
        ('pro', 'Оптимальный выбор'),
        ('ultra', 'Максимальная мощность'),
    ]
    
    category = models.ForeignKey(CategoryPC, on_delete=models.CASCADE, related_name='prebuilt_pcs')
    name = models.CharField('Название', max_length=100)
    level = models.CharField('Уровень', max_length=10, choices=LEVEL_CHOICES)
    level_color = models.CharField('Цвет уровня', max_length=20, default='blue-500')
    description = models.TextField('Описание', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Готовая сборка ПК'
        verbose_name_plural = 'Готовые сборки ПК'
        ordering = ['category', 'level', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.get_level_display()}"
    
    @property
    def total_price(self):
        """Общая стоимость сборки"""
        total = Decimal('0')
        for component in self.components.all():
            total += component.product.final_price * component.quantity
        return total
    
    def formatted_price(self):
        """Форматированная цена"""
        return f"{int(self.total_price):,}".replace(',', ' ') + ' ₽'

class PrebuiltPCComponent(models.Model):
    prebuilt_pc = models.ForeignKey(PrebuiltPC, on_delete=models.CASCADE, related_name='components')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('Количество', default=1)
    
    class Meta:
        verbose_name = 'Компонент готовой сборки'
        verbose_name_plural = 'Компоненты готовых сборок'
        unique_together = ('prebuilt_pc', 'category')
    
    def __str__(self):
        return f"{self.prebuilt_pc.name} - {self.product.name}"
