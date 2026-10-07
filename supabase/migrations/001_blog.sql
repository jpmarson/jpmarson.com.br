-- ============================================================================
-- Blog de jpmarson.com.br — esquema inicial
--
-- Uma tabela, um post por linha, português obrigatório e inglês opcional.
-- Leitura pública só de posts publicados; escrita só para o dono do blog.
-- ============================================================================

-- Dono do blog: único e-mail com permissão de escrita.
create or replace function public.is_blog_owner()
returns boolean
language sql
stable
set search_path = ''
as $$
  select coalesce((select auth.jwt() ->> 'email') = 'jpmarson@gmail.com', false);
$$;

comment on function public.is_blog_owner() is
  'Verdadeiro quando o usuário autenticado é o dono do blog (jpmarson@gmail.com).';


-- ----------------------------------------------------------------------------
-- Posts
-- ----------------------------------------------------------------------------
create table public.posts (
  id            uuid primary key default gen_random_uuid(),
  slug          text not null unique
                check (slug ~ '^[a-z0-9]+(-[a-z0-9]+)*$'),
  status        text not null default 'draft'
                check (status in ('draft', 'published')),
  published_at  date not null default current_date,

  -- português (obrigatório para publicar)
  title_pt      text not null default '',
  summary_pt    text not null default '',
  body_pt       text not null default '',
  tags_pt       text[] not null default '{}',

  -- inglês (opcional)
  title_en      text not null default '',
  summary_en    text not null default '',
  body_en       text not null default '',
  tags_en       text[] not null default '{}',

  created_at    timestamptz not null default now(),
  updated_at    timestamptz not null default now(),

  -- um post publicado precisa ter ao menos título e corpo em português
  constraint published_needs_pt check (
    status = 'draft' or (length(trim(title_pt)) > 0 and length(trim(body_pt)) > 0)
  )
);

comment on table public.posts is 'Posts do blog jpmarson.com.br (PT obrigatório, EN opcional).';
comment on column public.posts.slug is 'Parte da URL: jpmarson.com.br/blog/<slug>/';
comment on column public.posts.published_at is 'Data exibida no post e usada na ordenação.';

create index posts_status_published_at_idx on public.posts (status, published_at desc);


-- updated_at automático
create or replace function public.touch_updated_at()
returns trigger
language plpgsql
set search_path = ''
as $$
begin
  new.updated_at := now();
  return new;
end;
$$;

create trigger posts_touch_updated_at
  before update on public.posts
  for each row execute function public.touch_updated_at();


-- ----------------------------------------------------------------------------
-- Segurança (RLS)
-- ----------------------------------------------------------------------------
alter table public.posts enable row level security;

-- Qualquer visitante (e o gerador do site) lê apenas posts publicados.
create policy "Leitura pública de posts publicados"
  on public.posts for select
  to anon, authenticated
  using (status = 'published');

-- O dono lê tudo, inclusive rascunhos.
create policy "Dono lê todos os posts"
  on public.posts for select
  to authenticated
  using ((select public.is_blog_owner()));

create policy "Dono cria posts"
  on public.posts for insert
  to authenticated
  with check ((select public.is_blog_owner()));

create policy "Dono edita posts"
  on public.posts for update
  to authenticated
  using ((select public.is_blog_owner()))
  with check ((select public.is_blog_owner()));

-- Sem política de DELETE de propósito: posts são despublicados, não apagados.


-- ----------------------------------------------------------------------------
-- Imagens dos posts (Supabase Storage)
-- ----------------------------------------------------------------------------
insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values (
  'blog-images', 'blog-images', true, 5242880,  -- 5 MB
  array['image/png', 'image/jpeg', 'image/webp', 'image/gif', 'image/svg+xml']
)
on conflict (id) do nothing;

-- Bucket público: leitura pela URL pública, sem política de SELECT.
create policy "Dono envia imagens do blog"
  on storage.objects for insert
  to authenticated
  with check (bucket_id = 'blog-images' and (select public.is_blog_owner()));

create policy "Dono substitui imagens do blog"
  on storage.objects for update
  to authenticated
  using (bucket_id = 'blog-images' and (select public.is_blog_owner()))
  with check (bucket_id = 'blog-images' and (select public.is_blog_owner()));
