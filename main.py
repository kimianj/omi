from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from typing import Annotated
from fastapi import Query

# Configure FastAPI app
app = FastAPI()

# Add CORS middleware to allow all origins for the demo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
def home():
    """Main demo page to trigger the checkout sessions."""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>OMI - AI Wearable Platform | Promotion Codes Demo</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: #333;
                text-align: center;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                gap: 2rem;
            }
            .title {
                color: white;
                font-size: 2.5rem;
                font-weight: 700;
                margin-top: 2rem;
            }
            .controls {
                background: rgba(255,255,255,0.1);
                padding: 1.5rem;
                border-radius: 10px;
                margin-bottom: 2rem;
                color: white;
            }
            .btn {
                background: white;
                color: #667eea;
                border: none;
                padding: 0.5rem 1rem;
                border-radius: 5px;
                margin: 0.5rem;
                cursor: pointer;
                font-weight: bold;
                transition: transform 0.2s;
            }
            .btn:hover {
                transform: translateY(-2px);
            }
        </style>
    </head>
    <body>
        <h1 class="title">OMI Promotion Codes Demo</h1>
        <div class="controls">
            <h3>🎛️ Test Controls</h3>
            <p>Click a button to see the behavior in action.</p>
            <button class="btn" onclick="testWithPromoCodes()">
                Test WITH Promotion Codes
            </button>
            <button class="btn" onclick="testWithoutPromoCodes()">
                Test WITHOUT Promotion Codes
            </button>
        </div>
        
        <script>
            async function testWithPromoCodes() {
                window.location.href = '/demo-checkout?enable_promotion_codes=true';
            }
            async function testWithoutPromoCodes() {
                window.location.href = '/demo-checkout?enable_promotion_codes=false';
            }
        </script>
    </body>
    </html>
    """


# ---
# This is the only part you need to focus on.
# ---

@app.get("/demo-checkout", response_class=HTMLResponse)
def demo_checkout(
    enable_promotion_codes: Annotated[bool, Query()] = True
):
    """
    Simulates a Stripe checkout page. The presence of the promotion
    code box is controlled by the `enable_promotion_codes` query parameter.
    """
    
    # This is the core logic. It dynamically adds or removes the promo
    # section's CSS based on the boolean value.
    promo_section_style = ""
    if not enable_promotion_codes:
        promo_section_style = "display: none;"
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>OMI Checkout - Promotion Codes Demo</title>
        <style>
            body {{ 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: #f6f9fc;
                margin: 0;
                padding: 2rem;
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
            }}
            .checkout-container {{
                background: white;
                border-radius: 12px;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
                max-width: 500px;
                width: 100%;
                padding: 2rem;
            }}
            .stripe-header {{
                text-align: center;
                margin-bottom: 2rem;
                padding-bottom: 1rem;
                border-bottom: 1px solid #e6ebf1;
            }}
            .product-info {{
                display: flex;
                align-items: center;
                gap: 1rem;
                margin-bottom: 2rem;
                padding: 1rem;
                background: #f8fafc;
                border-radius: 8px;
            }}
            .product-image {{
                width: 60px;
                height: 60px;
                background: linear-gradient(135deg, #667eea, #764ba2);
                border-radius: 8px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-weight: bold;
            }}
            .product-details h3 {{
                margin: 0 0 0.5rem 0;
                color: #1a202c;
            }}
            .product-details p {{
                margin: 0;
                color: #718096;
                font-size: 0.9rem;
            }}
            .price {{
                font-weight: bold;
                color: #2d3748;
                margin-left: auto;
                font-size: 1.2rem;
            }}
            .form-group {{
                margin-bottom: 1.5rem;
            }}
            .form-group label {{
                display: block;
                margin-bottom: 0.5rem;
                color: #374151;
                font-weight: 500;
            }}
            .form-input {{
                width: 100%;
                padding: 0.75rem;
                border: 1px solid #d1d5db;
                border-radius: 6px;
                font-size: 1rem;
                transition: border-color 0.2s;
            }}
            .form-input:focus {{
                outline: none;
                border-color: #667eea;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            }}
            .promo-section {{
                background: #f0f9ff;
                border: 2px solid #bfdbfe;
                border-radius: 8px;
                padding: 1rem;
                margin-bottom: 1.5rem;
            }}
            .promo-toggle {{
                color: #1e40af;
                font-weight: 500;
                cursor: pointer;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }}
            .promo-input {{
                margin-top: 1rem;
                display: none;
            }}
            .promo-input.show {{
                display: block;
            }}
            .promo-success {{
                margin-top: 0.5rem;
                padding: 0.5rem;
                background: #dcfce7;
                border: 1px solid #16a34a;
                border-radius: 4px;
                color: #15803d;
                font-size: 0.9rem;
                display: none;
            }}
            .total-section {{
                background: #f8fafc;
                padding: 1rem;
                border-radius: 8px;
                margin-bottom: 2rem;
            }}
            .total-row {{
                display: flex;
                justify-content: space-between;
                margin-bottom: 0.5rem;
            }}
            .total-row.final {{
                font-weight: bold;
                font-size: 1.1rem;
                padding-top: 0.5rem;
                border-top: 1px solid #e5e7eb;
                margin-top: 0.5rem;
                margin-bottom: 0;
            }}
            .discount-row {{
                color: #059669;
                display: none;
            }}
            .pay-button {{
                width: 100%;
                background: #667eea;
                color: white;
                border: none;
                padding: 1rem;
                border-radius: 6px;
                font-size: 1.1rem;
                font-weight: 600;
                cursor: pointer;
                transition: background 0.2s;
            }}
            .pay-button:hover {{
                background: #5a67d8;
            }}
            .demo-badge {{
                position: fixed;
                top: 20px;
                right: 20px;
                background: #f59e0b;
                color: white;
                padding: 0.5rem 1rem;
                border-radius: 20px;
                font-weight: bold;
                font-size: 0.9rem;
                z-index: 1000;
            }}
            .demo-instructions {{
                background: #fffbeb;
                border: 1px solid #f59e0b;
                border-radius: 8px;
                padding: 1rem;
                margin-bottom: 2rem;
                font-size: 0.9rem;
            }}
        </style>
    </head>
    <body>
        <div class="demo-badge">🎯 DEMO MODE</div>
        
        <div class="checkout-container">
            <div class="stripe-header">
                <h2>Complete your order</h2>
                <p style="color: #6b7280; margin: 0;">Powered by Stripe</p>
            </div>
            
            <div class="demo-instructions" style="background:#dcfce7;border-color:#16a34a;color:#15803d;">
                <strong>✅ This is how OMI's checkout would look {'WITH' if enable_promotion_codes else 'WITHOUT'} promotion codes!</strong><br>
                Look for the "Add promotion code" link below.
            </div>
            
            <div class="product-info">
                <div class="product-image">OMI</div>
                <div class="product-details">
                    <h3>OMI Dev Kit 2</h3>
                    <p>Real-time conversation transcription</p>
                </div>
                <div class="price">$69.99</div>
            </div>
            
            <div class="form-group">
                <label>Email</label>
                <input type="email" class="form-input" placeholder="Enter your email" value="demo@example.com">
            </div>
            
            <div class="form-group">
                <label>Card information</label>
                <input type="text" class="form-input" placeholder="4242 4242 4242 4242" value="4242 4242 4242 4242">
                <div style="display: flex; gap: 0.5rem; margin-top: 0.5rem;">
                    <input type="text" class="form-input" placeholder="MM / YY" value="12 / 25" style="flex: 1;">
                    <input type="text" class="form-input" placeholder="CVC" value="123" style="flex: 1;">
                </div>
            </div>
            
            <div class="promo-section" style="{promo_section_style}">
                <div class="promo-toggle" onclick="togglePromoCode()">
                    <span id="promo-icon">+</span>
                    <span>Add promotion code</span>
                </div>
                <div class="promo-input" id="promo-input">
                    <input type="text" placeholder="Enter promotion code" id="promo-code" oninput="checkPromoCode()">
                    <div class="promo-success" id="promo-success">
                        ✅ Promotion code "SAVE20" applied! You saved $14.00
                    </div>
                </div>
            </div>
            
            <div class="total-section">
                <div class="total-row">
                    <span>Subtotal</span>
                    <span>$69.99</span>
                </div>
                <div class="total-row discount-row" id="discount-row">
                    <span>Discount (SAVE20)</span>
                    <span>-$14.00</span>
                </div>
                <div class="total-row final">
                    <span>Total</span>
                    <span id="final-total">$69.99</span>
                </div>
            </div>
            
            <button class="pay-button" onclick="simulatePayment()">
                Pay <span id="pay-amount">$69.99</span>
            </button>
            
            <div style="text-align: center; margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #e5e7eb;">
                <p style="color: #6b7280; font-size: 0.9rem; margin: 0;">
                    🔒 This demo shows how OMI checkout would work with promotion codes enabled<br>
                    <strong>Implementation:</strong> Just add <code>allow_promotion_codes=True</code> to Stripe checkout
                </p>
            </div>
        </div>
        
        <script>
            function togglePromoCode() {{
                const input = document.getElementById('promo-input');
                const icon = document.getElementById('promo-icon');
                
                if (input.classList.contains('show')) {{
                    input.classList.remove('show');
                    icon.textContent = '+';
                }} else {{
                    input.classList.add('show');
                    icon.textContent = '−';
                    document.getElementById('promo-code').focus();
                }}
            }}
            
            function checkPromoCode() {{
                const code = document.getElementById('promo-code').value.toUpperCase();
                const success = document.getElementById('promo-success');
                const discountRow = document.getElementById('discount-row');
                const finalTotal = document.getElementById('final-total');
                const payAmount = document.getElementById('pay-amount');
                
                if (code === 'SAVE20' || code === 'DISCOUNT20' || code === 'OMI20') {{
                    success.style.display = 'block';
                    discountRow.style.display = 'flex';
                    finalTotal.textContent = '$55.99';
                    payAmount.textContent = '$55.99';
                }} else {{
                    success.style.display = 'none';
                    discountRow.style.display = 'none';
                    finalTotal.textContent = '$69.99';
                    payAmount.textContent = '$69.99';
                }}
            }}
            
            function simulatePayment() {{
                alert('🎉 Demo Complete!\\n\\nThis shows exactly how OMI customers would:\\n✅ See promotion code option\\n✅ Enter discount codes\\n✅ Get automatic price updates\\n✅ Complete purchase with discount\\n\\nImplementation: Just add allow_promotion_codes=True to your Stripe checkout!');
            }}
        </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
