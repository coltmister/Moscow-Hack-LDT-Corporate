import { Post } from '@/components';
import { MainLayout } from '@/layouts';
import { useState } from 'react';
import { useGetAllPostsQuery } from '../../../services/Feed.service';
import { FeedSidebarFilters } from '../../common/Feed/FeedSidebarFilters';
import { Pagination } from '@mui/material';
import { SidebarFilters } from '../../common/SidebarFilters';

export const Index = () => {
    const [page, setPage] = useState(1);
    const [sortDesc, setSortDesc] = useState(false);

    const { data: posts, refetch } = useGetAllPostsQuery({ page, sortDesc });

    return (
        <MainLayout sidebarTitle='Фильтр' sidebarNode={<SidebarFilters sortDesc={sortDesc} setDesc={setSortDesc} />}>
            <section>
                {posts?.payload?.map((item) => (
                    <Post
                        created_at={item.created_at}
                        key={item.id}
                        author={item.author.snp}
                        avatar={item.author.avatar ?? ''}
                        id={item.id}
                        title={item.title}
                        reactions={item.reactions}
                        my_reaction={item.my_reaction}
                        authorId={item.author.id}
                        ideaId={item.idea.id}
                        onLike={refetch}
                        description={item.description}
                    />
                ))}
            </section>
            {!!posts?.payload?.length && (
                <Pagination className='mb-15' count={posts?.total_pages} onChange={(event, page) => setPage(page)} />
            )}
        </MainLayout>
    );
};
