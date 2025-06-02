// src/components/GradebookForm/index.jsx
import styles from './gradebookForm.module.css';

export default function GradebookForm({ initialData, onSubmit }) {
  const [formData, setFormData] = useState(initialData || {});
  const [errors, setErrors] = useState({});

  const validate = () => {
    const newErrors = {};
    if (!formData.name) newErrors.name = 'Название обязательно';
    if (formData.class?.length > 10) newErrors.class = 'Слишком длинное название класса';
    return newErrors;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const validationErrors = validate();
    if (Object.keys(validationErrors).length === 0) {
      onSubmit(formData);
    } else {
      setErrors(validationErrors);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <FormField
        label="Название журнала"
        error={errors.name}
        inputProps={{
          value: formData.name,
          onChange: (e) => setFormData({...formData, name: e.target.value})
        }}
      />
      
      <FormField
        label="Класс"
        error={errors.class}
        inputProps={{
          value: formData.class,
          onChange: (e) => setFormData({...formData, class: e.target.value})
        }}
      />

      <FormToggle
        label="Архивный журнал"
        checked={formData.status === 'archived'}
        onChange={(checked) => 
          setFormData({...formData, status: checked ? 'archived' : 'active'})
        }
      />

      <FormActions>
        <Button type="submit">Сохранить</Button>
        <Button type="button" variant="secondary">Отмена</Button>
      </FormActions>
    </form>
  );
}