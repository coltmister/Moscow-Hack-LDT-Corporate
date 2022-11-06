from django.contrib import admin

from ideas.models import Idea, IdeaStatusHistory, IdeaInformation, IdeaComment, IdeaLike, IdeaCategory, \
    IdeaSettings, IdeaDocument, Post, PostLike, PostComment


class IdeaAdmin(admin.ModelAdmin):
    def get_obj_id(self, obj):
        return f"✏️{obj.id}"

    get_obj_id.short_description = 'ID'

    list_display = (
        'get_obj_id', 'title', 'description', 'author', 'team', 'created_at'
    )

    search_fields = ['id', 'title', 'description', 'author__snp', 'author__username']
    readonly_fields = ('id', 'created_at', 'updated_at')
    fieldsets = (
        ('Основные сведения', {
            'fields': (
                'id', 'title', 'description', 'author',
                'idea_json', 'status', 'category', 'tags', 'links', 'rating',
                'subscribers'
            )
        }),
        ('Дополнительные сведения', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at'),
        }),
    )


admin.site.register(Idea, IdeaAdmin)
admin.site.register(IdeaStatusHistory)
admin.site.register(IdeaInformation)
admin.site.register(IdeaComment)
admin.site.register(IdeaLike)
admin.site.register(IdeaCategory)
admin.site.register(IdeaSettings)
admin.site.register(IdeaDocument)
admin.site.register(Post)
admin.site.register(PostLike)
admin.site.register(PostComment)
