import { MainLayout } from '@/layouts';
import { Post } from '@/components';
import { useGetAllIdeasQuery } from '@/services';
import { SidebarFilters } from '../../common/SidebarFilters';
import { useEffect, useState } from 'react';
import { Pagination } from '@mui/material';
import { FeedSidebarFilters } from '../../common/Feed/FeedSidebarFilters';

export const Ideas = () => {
    const [sortDesc, setSortDesc] = useState(false);
    const [limit, setLimit] = useState(false);
    const [postsPerPage, setPostsPerPage] = useState(5);
    const [category, setCategory] = useState('new');

    const [page, setPage] = useState(1);
    const { data, refetch } = useGetAllIdeasQuery(
        { sortDesc, limit: postsPerPage, page, feed_param: category },
        {
            refetchOnMountOrArgChange: true,
        }
    );

    useEffect(() => {
        if (limit) {
            setPostsPerPage(10);
        } else {
            setPostsPerPage(5);
        }
    }, [limit]);

    return (
        <MainLayout
            sidebarTitle='Фильтры'
            sidebarNode={
                <>
                    <SidebarFilters sortDesc={sortDesc} setDesc={setSortDesc} setLimit={setLimit} limit={limit} />
                    <br />
                    <FeedSidebarFilters setCategory={setCategory} />
                </>
            }
        >
            {data?.payload.map((idea) => (
                <Post
                    key={idea.id}
                    mode='ideas'
                    description={idea.description}
                    title={idea.title}
                    author={idea.author.snp}
                    id={idea.id}
                    authorId={idea.author.id}
                    avatar={undefined}
                    reactions={idea.reactions}
                    my_reaction={idea.my_reaction}
                    created_at={idea.created_at}
                    onLike={refetch}
                />
            ))}
            {!!data?.payload?.length && (
                <Pagination className='mb-15' count={data?.total_pages} onChange={(event, page) => setPage(page)} />
            )}
        </MainLayout>
    );
};
