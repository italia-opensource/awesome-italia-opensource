// Make sure to run npm install @formspree/react
// For more help visit https://formspr.ee/react-help
import React from 'react';
import { useForm, ValidationError } from '@formspree/react';
import styles from './styles.module.css';

export default function NewsletterForm() {
    const [state, handleSubmit] = useForm("xoqbqong");
    if (state.succeeded) {
        return <p>Thanks for joining!</p>;
    }
    return (

        <div className={styles.wrapper}>
        <form onSubmit={handleSubmit}>
            <div className="form-input">
                <input
                    id="email"
                    type="email" 
                    name="email"
                    placeholder='Email Address'
                    className={styles.form_input}
                    required
                />
                <ValidationError 
                    prefix="Email" 
                    field="email"
                    errors={state.errors}
                />
                
                <button type="submit" disabled={state.submitting} className={styles.subscribe}>
                    Subscribe
                </button>

            <div className={styles.notice}>
                <input type="checkbox" name="subscribe" value="newsletter" required />
                <span>I agree to my email address being stored and uses to recieve monthly newsletter.</span>
            </div>
            </div>
        </form>
        </div>
    );
}