import FormEdit from './FormEdit';
import FormView from './FormView';
import { useState } from 'react';
import { useAppropriateUserForm } from '../../../../../hooks/useAppropriateUserForm';

const Form = () => {
    const { data } = useAppropriateUserForm();
    const [isEditing, setIsEditing] = useState(false);
    return (
        <>
            {data && isEditing && <FormEdit data={data} setIsEditing={setIsEditing} />}
            {data && !isEditing && <FormView data={data} setIsEditing={setIsEditing} />}
        </>
    );
};

export default Form;
