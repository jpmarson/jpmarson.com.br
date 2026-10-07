-- Unifica as duas políticas de leitura para usuários autenticados numa só
-- (recomendação do Supabase Advisor: multiple_permissive_policies).
-- Mesmo resultado de antes: visitantes veem só publicados; o dono vê tudo.

drop policy "Leitura pública de posts publicados" on public.posts;
drop policy "Dono lê todos os posts" on public.posts;

create policy "Visitantes leem posts publicados"
  on public.posts for select
  to anon
  using (status = 'published');

create policy "Logados leem publicados; dono lê tudo"
  on public.posts for select
  to authenticated
  using (status = 'published' or (select public.is_blog_owner()));
