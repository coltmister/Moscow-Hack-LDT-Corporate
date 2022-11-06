import { useParams } from 'react-router-dom';
import { Post } from '@/components';
import { useGetAllPostsQuery, useGetPostQuery, useGetPostsByIdQuery } from '@/services';
import { MainLayout } from '@/layouts';

const PostPage = () => {
    const id = useParams().id;
    const { data: post, refetch } = useGetAllPostsQuery({ limit: 200, page: 1, search: '', desc: true });

    const postToRender = post?.payload.filter((el) => el.id === id)[0];

    return (
        <MainLayout hideFilters contentFullWidth>
            {postToRender && (
                <Post
                    id={postToRender?.id}
                    title={postToRender?.title}
                    description={postToRender?.description}
                    author={postToRender?.author?.snp}
                    authorId={postToRender?.author?.id}
                    ideaId={postToRender?.idea.id}
                    created_at={postToRender?.created_at}
                    reactions={postToRender?.reactions}
                    my_reaction={postToRender?.my_reaction}
                    onLike={refetch}
                    mode={'posts'}
                />
            )}
        </MainLayout>
    );
};

export default PostPage;
