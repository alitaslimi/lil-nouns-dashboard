# Libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.subplots as sp
import plotly.graph_objects as go
import PIL

# Page Favicon
favicon = PIL.Image.open('favicon.ico')

# Global Variables
theme_plotly = None # None or streamlit

# Layout
st.set_page_config(page_title='Lil Nouns', page_icon=favicon, layout='wide')
st.title('Lil Nouns')

# Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

# Data Sources
# @st.cache(ttl=3600)
def get_data(query):
    if query == 'Mints Overview':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/c88b2d6a-158b-4b1a-bc18-0a3920ada097/data/latest')
    elif query == 'Mints Daily':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/ab1699c8-24c2-49cc-b8fe-09f50e2cfd7f/data/latest')
    elif query == 'Traits':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/b82c2f87-3a01-447d-934a-0f56f10dc975/data/latest')
    elif query == 'Rarity':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/32069d6d-a488-41de-acd7-f92fe3afce7a/data/latest')
    elif query == 'Sales Overview':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/953f9a9c-2949-4332-80fb-a574b853ae2e/data/latest')
    elif query == 'Sales Daily':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/6288a2b2-f155-48f5-abdd-edb2ad0c29ea/data/latest')
    elif query == 'Sales Marketplaces':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/6f9384a0-e8e2-4ea2-bd4d-30a19bfe1b92/data/latest')
    elif query == 'Holders Overview':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/2a662aed-54bc-4a5d-95ff-fb113ff36089/data/latest')
    elif query == 'Holders Holdings':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/7d5f3df4-33b7-49a2-9afb-06fd355f299e/data/latest')
    elif query == 'Holders Distribution':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/25621d2e-9779-4a2e-93be-b516f6507e25/data/latest')
    elif query == 'Proposals Overview':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/04a97aa4-8a2d-4378-92fe-87fccaadbc60/data/latest')
    elif query == 'Votes Overview':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/ad3f18ce-0807-48a5-acc1-4417bd6437d6/data/latest')
    elif query == 'Votes Options':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/42c4e655-b154-409a-9e70-05057e838a8d/data/latest')
    return None

mints_overview = get_data('Mints Overview')
mints_daily = get_data('Mints Daily')
sales_overview = get_data('Sales Overview')
sales_daily = get_data('Sales Daily')
sales_marketplaces = get_data('Sales Marketplaces')
holders_overview = get_data('Holders Overview')
holders_holdings = get_data('Holders Holdings')
holders_distribution = get_data('Holders Distribution')
proposals_overview = get_data('Proposals Overview')
votes_overview = get_data('Votes Overview')
votes_options = get_data('Votes Options')

traits = get_data('Traits')
traits_backgrounds = pd.read_csv('traits_backgrounds.csv')
traits_bodies = pd.read_csv('traits_bodies.csv')
traits_accessories = pd.read_csv('traits_accessories.csv')
traits_heads = pd.read_csv('traits_heads.csv')
traits_glasses = pd.read_csv('traits_glasses.csv')

backgrounds = pd.Series(traits_backgrounds.Name, index=traits_backgrounds.ID.values).to_dict()
bodies = pd.Series(traits_bodies.Name, index=traits_bodies.ID.values).to_dict()
accessories = pd.Series(traits_accessories.Name, index=traits_accessories.ID.values).to_dict()
heads = pd.Series(traits_heads.Name, index=traits_heads.ID.values).to_dict()
glasses = pd.Series(traits_glasses.Name, index=traits_glasses.ID.values).to_dict()

traits["Background"] = traits["Background"].map(backgrounds)
traits["Body"] = traits["Body"].map(bodies)
traits["Accessory"] = traits["Accessory"].map(accessories)
traits["Head"] = traits["Head"].map(heads)
traits["Glasses"] = traits["Glasses"].map(glasses)

traits_rarity = get_data('Rarity')
traits_rarity["Background"] = traits_rarity["Background"].map(backgrounds)
traits_rarity["Body"] = traits_rarity["Body"].map(bodies)
traits_rarity["Accessory"] = traits_rarity["Accessory"].map(accessories)
traits_rarity["Head"] = traits_rarity["Head"].map(heads)
traits_rarity["Glasses"] = traits_rarity["Glasses"].map(glasses)

# Content
st.header('Introduction')

c1, c2 = st.columns([2, 1])
with c1:
    st.write(
        """
        [Lil Nouns](https://lilnouns.wtf) is a generative non-fungible token (NFT) project on the
        Ethereum blockchain which has been forked from [Nouns](https://nouns.wtf). Each Lil Nouns
        NFT is a 32x32 pixel character with various traits. Every 15 minutes, a Lil Noun is generated,
        forever. After a new Lil Noun spawns into the world, an auction will take place to sell
        that NFT. The main interface for participating in the auctions is Lil Nouns official website
        maintained by the founders of the project.

        The Lil Nouns DAO treasury receives 100% of ETH proceeds from daily noun auctions. It is the
        main governing body of the Lil Nouns ecosystem. Each Lil Noun is entitled to one vote in all
        governance matters. Lil Nouns Holders can utilize their voting power (1 Lil Noun = 1 vote) to
        direct the treasury. They can propose new ideas or vote on the existing ones which will be
        executed on the Ethereum blockchain when they are approved. Currently, a minimum of 7 Lil Nouns
        is required for a holder to submit proposals. The voting power of Lil Nouns can also be
        delegated to a third party.

        Lil Nounders is the term attributed to the group of builders that initiated Lil Nouns. As
        100% of Lil Noun auction earnings are sent to the DAO, they have chosen to compensate themselves
        with one every 10th Lil Noun, starting from #0, for the first five years. These Lil Nouns
        will be automatically sent to a multi-signature address shared among the founding members.
        Lil Nounders have also chosen to compensate the Nouns DAO with Lil Nouns. Every 10th Lil Noun
        starting from #1 for the first five years will be sent to the Nouns DAO treasury and shared
        among the members of the project.
        """
    )
with c2:
    image = PIL.Image.open('lil-nouns-classroom.png')
    st.image(image)

with st.expander('**Methodology**'):
    st.write(
        """
        The data for this dashboard was selected from the [**Flipside Crypto**](https://flipsidecrypto.xyz)
        data platform by using its **REST API**. These queries are currently set to **re-run every 24 hours** to
        cover the latest data and are imported as a JSON file. The code for this tool is saved and accessible
        in its [**GitHub Repository**](https://github.com/alitaslimi/lil-nouns-dashboard).

        This dashboard is designed and structured in multiple **Tabs** that are accessible under the **Analysis**
        section. Each of these Tabs addresses a different segment of the Lil Nouns DAO (Mints, Sales, Holders,
        Governance, etc.).
        
        **Contract Addresses:**
        - Lil Nouns NFT: [0x4b10701bfd7bfedc47d50562b76b436fbb5bdb3b](https://etherscan.io/token/0x4b10701bfd7bfedc47d50562b76b436fbb5bdb3b)
        - Lil Nounders Multi-Sig: [0x3cf6a7f06015acad49f76044d3c63d7fe477d945](https://etherscan.io/address/0x3cf6a7f06015acad49f76044d3c63d7fe477d945)
        - Nouns DAO Treasury: [0x0bc3807ec262cb779b38d65b38158acc3bfede10](https://etherscan.io/address/0x0bc3807ec262cb779b38d65b38158acc3bfede10)
        - Lil Nouns Initiator: [0xa6ef22a84521ddd11c1282ec8f8a9255dbac04a0](https://etherscan.io/address/0xa6ef22a84521ddd11c1282ec8f8a9255dbac04a0)
        - Nouns DAO Executer: [0xd5f279ff9eb21c6d40c8f345a66f2751c4eea1fb](https://etherscan.io/address/0xd5f279ff9eb21c6d40c8f345a66f2751c4eea1fb)
        """
    )

st.header('Analysis')

st.write(
    """
    The hyper-inflationary nature of Lil Nouns makes its NFTs different from other collections. It
    should be noted that these NFTs act as a key to access the DAO and the decisions that are being
    made for its treasury. The constant minting of the Lil Nouns puts their focus on their voting
    power for their holders, in comparison to the financial gain of NFTs of other collections.
    Considering this, although the primary and secondary sales data are presented in this dashboard,
    the focus of the analysis was on governance and user engagement with the proposals submitted to
    the DAO.
    """
)

tab_mints, tab_sales, tab_traits, tab_holders, tab_governance = st.tabs(['**Mints**', '**Sales**', '**Traits**', '**Holders**', '**Governance**'])

with tab_mints:

    st.write(
        """
        Lil Nouns are being distributed using an on-chain auction every 15 minutes. In other words,
        the minting (primary sales) process of these NFTs is conducted using a bidding mechanism.
        After the conclusion of the bidding of every 9th Lil Noun (#9, #19, #29 and so on), the 10th
        and 11th Lil Nouns are automatically minted and transferred to the wallet address of Lil Nouns
        DAO and Lil Nounders. With that being said, the data in this section only represents the
        result of auctions and shows the initial distribution of Lil Nouns. It is worth mentioning
        that if no one bids on a Lil Noun, it will be burned and sent to a NULL address. Holders also
        are able to burn their tokens, resulting in the reduction of the total number of circulating
        NFTs. The data regarding the exact number of Lil Nouns supply are available on the **Holders**
        tab.
        """
    )

    st.subheader('Overview')

    df = mints_overview
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric(label='**Unique Auctioners**', value=str(df['Auctioners'].map('{:,.0f}'.format).values[0]), help='Minters')
        st.metric(label='**Auctioned Lil Nouns**', value=str(df['AuctionedNFTs'].map('{:,.0f}'.format).values[0]))
    with c2:
        st.metric(label='**Average Mint Price**', value=str(df['MintPrice'].map('{:,.2f}'.format).values[0]), help='ETH')
        st.metric(label='**Lil Nouns Allocated to Treasury**', value=str(df['TreasuryNFTs'].map('{:,.0f}'.format).values[0]))
    with c3:
        st.metric(label='**Burned Lil Nouns**', value=str(df['BurnedNFTs'].map('{:,.0f}'.format).values[0]))
        st.metric(label='**Lil Nouns Allocated to Lil Nounders**', value=str(df['LilNoundersNFTs'].map('{:,.0f}'.format).values[0]))
    
    st.subheader('Activity Over Time')

    interval = st.radio('**Time Interval**', ['Daily', 'Weekly', 'Monthly'], key='mints_interval', horizontal=True)

    if st.session_state.mints_interval == 'Daily':
        df = mints_daily
    elif st.session_state.mints_interval == 'Weekly':
        df = mints_daily
        df = df.groupby(pd.Grouper(freq='W', key='Date')).agg(
            {'Minters': 'sum', 'MintedNFTs': 'sum', 'BurnedNFTs': 'sum', 'Volume': 'sum', 'VolumeUSD': 'sum', 'Price': 'mean', 'PriceUSD': 'mean'}).reset_index()
    elif st.session_state.mints_interval == 'Monthly':
        df = mints_daily
        df = df.groupby(pd.Grouper(freq='MS', key='Date')).agg(
            {'Minters': 'sum', 'MintedNFTs': 'sum', 'BurnedNFTs': 'sum', 'Volume': 'sum', 'VolumeUSD': 'sum', 'Price': 'mean', 'PriceUSD': 'mean'}).reset_index()

    fig = sp.make_subplots(specs=[[{'secondary_y': True}]])
    fig.add_trace(go.Bar(x=df['Date'], y=df['Volume'], name='ETH Volume', hovertemplate='%{y:,.2f} ETH<extra></extra>'), secondary_y=False)
    fig.add_trace(go.Line(x=df['Date'], y=df['VolumeUSD'], name='USD Volume', hovertemplate='%{y:,.0f} USD<extra></extra>'), secondary_y=True)
    fig.update_layout(title_text='Minted Volume Over Time', hovermode='x unified')
    fig.update_yaxes(title_text='Volume [ETH]', secondary_y=False, rangemode='tozero')
    fig.update_yaxes(title_text='Volume [USD]', secondary_y=True, rangemode='tozero')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    fig = sp.make_subplots()
    fig.add_trace(go.Bar(x=df['Date'], y=df['Minters'], name='Minters', hovertemplate='Minters: %{y:,.0f}<extra></extra>'))
    fig.add_trace(go.Line(x=df['Date'], y=df['MintedNFTs'], name='Lil Nouns', hovertemplate='Lil Nouns: %{y:,.0f}<extra></extra>'))
    fig.update_layout(title_text='Number of Minters and Minted Lil Nouns Over Time', yaxis_title='Addresses', hovermode='x unified')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    fig = sp.make_subplots(specs=[[{'secondary_y': True}]])
    fig.add_trace(go.Bar(x=df['Date'], y=df['Price'], name='ETH Price', hovertemplate='%{y:,.4f} ETH<extra></extra>'), secondary_y=False)
    fig.add_trace(go.Line(x=df['Date'], y=df['PriceUSD'], name='USD Price', hovertemplate='%{y:,.0f} USD<extra></extra>'), secondary_y=True)
    fig.update_layout(title_text='Average Mint Price Over Time', hovermode='x unified')
    fig.update_yaxes(title_text='Price [ETH]', secondary_y=False, rangemode='tozero')
    fig.update_yaxes(title_text='Price [USD]', secondary_y=True, rangemode='tozero')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    fig = px.bar(df, x='Date', y='BurnedNFTs', title='Burned Lil Nouns Over Time')
    fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title='Number of Lil Nouns', hovermode='x unified')
    fig.update_traces(hovertemplate='Lil Nouns: %{y:,.0f}<extra></extra>')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

with tab_sales:

    st.write(
        """
        The secondary sales data of Lil Nouns are presented in this section. A considerable number
        of addresses have bought Lil Nouns through NFT marketplaces, especially OpenSea, since the
        current average price of these NFTs is slightly below the 1.5 ETH that is required to bid
        on their auctions.
        """
    )

    st.subheader('Overview')
    
    df = sales_overview
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric(label='**Total Sales Volume**', value=str(df['Volume'].map('{:,.0f}'.format).values[0]), help='USD')
        st.metric(label='**Average Daily Volume**', value=str(df['Volume/Day'].map('{:,.0f}'.format).values[0]), help='USD')
    with c2:
        st.metric(label='**Total Sales**', value=str(df['Sales'].map('{:,.0f}'.format).values[0]))
        st.metric(label='**Average Daily Sales**', value=str(df['Sales/Day'].map('{:,.0f}'.format).values[0]))
    with c3:
        st.metric(label='**Total Unique Buyers**', value=str(df['Buyers'].map('{:,.0f}'.format).values[0]))
        st.metric(label='**Average Daily Buyers**', value=str(df['Buyers/Day'].map('{:,.0f}'.format).values[0]))
    with c4:
        st.metric(label='**Total Traded NFTs**', value=str(df['NFTs'].map('{:,.0f}'.format).values[0]))
        st.metric(label='**Average Daily Traded NFTs**', value=str(df['NFTs/Day'].map('{:,.0f}'.format).values[0]))

    st.subheader('Prices')

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric(label='**Average Price of Lil Nouns**', value=str(df['PriceAverage'].map('{:,.2f}'.format).values[0]), help='USD')
    with c2:
        st.metric(label='**Median Price of Lil Nouns**', value=str(df['PriceMedian'].map('{:,.2f}'.format).values[0]), help='USD')
    with c3:
        st.metric(label='**Price of the Most Expensive Lil Noun**', value=str(df['PriceMax'].map('{:,.2f}'.format).values[0]), help='USD')
    with c4:
        st.metric(label='**Price of the Cheapest Lil Noun**', value=str(df['PriceMin'].map('{:,.2f}'.format).values[0]), help='USD')

    st.subheader('Marketplaces')

    df = sales_marketplaces
    c1, c2, c3 = st.columns(3)
    with c1:
        fig = px.pie(df, values='Volume', names='Marketplace', title='Share of Total Sales Volume [USD]', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        fig = px.pie(df, values='Sales', names='Marketplace', title='Share of Total Sales', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c3:
        fig = px.pie(df, values='Buyers', names='Marketplace', title='Share of Total Unique Buyers', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    
    st.subheader('Activity Over Time')

    interval = st.radio('**Time Interval**', ['Daily', 'Weekly', 'Monthly'], key='sales_interval', horizontal=True)

    if st.session_state.sales_interval == 'Daily':
        df = sales_daily
    elif st.session_state.sales_interval == 'Weekly':
        df = sales_daily
        df = df.groupby(pd.Grouper(freq='W', key='Date')).agg(
            {'Sales': 'sum', 'Buyers': 'sum', 'Sellers': 'sum', 'NFTs': 'sum', 'Volume': 'sum', 'Price': 'mean'}).reset_index()
    elif st.session_state.sales_interval == 'Monthly':
        df = sales_daily
        df = df.groupby(pd.Grouper(freq='MS', key='Date')).agg(
            {'Sales': 'sum', 'Buyers': 'sum', 'Sellers': 'sum', 'NFTs': 'sum', 'Volume': 'sum', 'Price': 'mean'}).reset_index()

    fig = sp.make_subplots(specs=[[{'secondary_y': True}]])
    fig.add_trace(go.Bar(x=df['Date'], y=df['Volume'], name='Volume', hovertemplate='Volume: %{y:,.0f} USD<extra></extra>'), secondary_y=False)
    fig.add_trace(go.Line(x=df['Date'], y=df['Price'], name='Price', hovertemplate='Price: %{y:,.0f} USD<extra></extra>'), secondary_y=True)
    fig.update_layout(title_text='Sales Volume and Average NFT Price Over Time', hovermode='x unified')
    fig.update_yaxes(title_text='Volume [USD]', secondary_y=False, rangemode='tozero')
    fig.update_yaxes(title_text='Price [USD]', secondary_y=True, rangemode='tozero')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    fig = sp.make_subplots()
    fig.add_trace(go.Bar(x=df['Date'], y=df['Sales'], name='Sales', hovertemplate='Sales: %{y:,.0f}<extra></extra>'))
    fig.add_trace(go.Line(x=df['Date'], y=df['NFTs'], name='Lil Nouns', hovertemplate='Lil Nouns: %{y:,.0f}<extra></extra>'))
    fig.update_layout(title_text='Number of Sales and Traded NFTs Over Time', yaxis_title='Numbers', hovermode='x unified')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    fig = sp.make_subplots()
    fig.add_trace(go.Bar(x=df['Date'], y=df['Buyers'], name='Buyers', hovertemplate='Buyers: %{y:,.0f}<extra></extra>'))
    fig.add_trace(go.Line(x=df['Date'], y=df['Sellers'], name='Sellers', hovertemplate='Sellers: %{y:,.0f}<extra></extra>'))
    fig.update_layout(title_text='Number of Buyers and Sellers Over Time', yaxis_title='Addresses', hovermode='x unified')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

with tab_traits:

    st.write(
        """
        Although each Lil Noun has four unique traits, except its background, they have little to
        no impact on the price of these NFTs. This section is just for enthusiast holders to see
        how common or rare their Lil Noun is.
        """
    )

    st.subheader('Overview')

    c1, c2 = st.columns(2)
    with c1:
        df = traits.groupby('Body').agg({'NFT': 'count'}).sort_values(by='NFT', ascending=False).reset_index()
        df.loc[df.index >= 10, 'Body'] = 'Other'
        fig = px.pie(df, values='NFT', names='Body', title='The Most Common Body Traits', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        df = traits.groupby('Accessory').agg({'NFT': 'count'}).sort_values(by='NFT', ascending=False).reset_index()
        df.loc[df.index >= 10, 'Accessory'] = 'Other'
        fig = px.pie(df, values='NFT', names='Accessory', title='The Most Common Accessory Traits', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        df = traits.groupby('Head').agg({'NFT': 'count'}).sort_values(by='NFT', ascending=False).reset_index()
        df.loc[df.index >= 10, 'Head'] = 'Other'
        fig = px.pie(df, values='NFT', names='Head', title='The Most Common Head Traits', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        df = traits.groupby('Glasses').agg({'NFT': 'count'}).sort_values(by='NFT', ascending=False).reset_index()
        df.loc[df.index >= 10, 'Glasses'] = 'Other'
        fig = px.pie(df, values='NFT', names='Glasses', title='The Most Common Glasses Traits', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        df = traits.groupby('Body').agg({'NFT': 'count'}).sort_values(by='NFT', ascending=True).reset_index().head(10)
        fig = px.bar(df, x='Body', y='NFT', color='Body', title='The Most Rare Body Traits')
        fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title='Number of Lil Nouns')
        fig.update_xaxes(type='category', categoryorder='total descending')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        df = traits.groupby('Accessory').agg({'NFT': 'count'}).sort_values(by='NFT', ascending=True).reset_index().head(10)
        fig = px.bar(df, x='Accessory', y='NFT', color='Accessory', title='The Most Rare Accessory Traits')
        fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title='Number of Lil Nouns')
        fig.update_xaxes(type='category', categoryorder='total descending')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        df = traits.groupby('Head').agg({'NFT': 'count'}).sort_values(by='NFT', ascending=True).reset_index().head(10)
        fig = px.bar(df, x='Head', y='NFT', color='Head', title='The Most Rare Head Traits')
        fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title='Number of Lil Nouns')
        fig.update_xaxes(type='category', categoryorder='total descending')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        df = traits.groupby('Glasses').agg({'NFT': 'count'}).sort_values(by='NFT', ascending=True).reset_index().head(10)
        fig = px.bar(df, x='Glasses', y='NFT', color='Glasses', title='The Most Rare Glasses Traits')
        fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title='Number of Lil Nouns')
        fig.update_xaxes(type='category', categoryorder='total descending')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    
    with st.expander('**Rarity of Lil Nouns**', expanded=True):
        st.write(
            """
            The **Rarity** columns are all in percent. The value means that only X% of the Lil Nouns
            have traits similar to this Lil Noun. Since the traits are almost equally distributed,
            the rarity of all the Lil Nouns is quite close to one another.
            """
        )
        df = traits_rarity.sort_values(by='Rarity', ascending=True).reset_index(drop=True)
        df.index += 1
        st.dataframe(df, use_container_width=True)

with tab_holders:

    st.write(
        """
        This section covers the most updated holders' information on Lil Nouns considering all
        token transfers (mints, sales, and burns) to determine the accurate number of NFTs
        each holder holds. This is important since Lil Nouns give their holders the voting power
        for participation in proposals.
        """
    )

    st.subheader('Overview')
    
    df = holders_overview
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric(label='**Total Unique Holders**', value=str('{:,.0f}'.format(df['Holders'].agg('sum'))))
        st.metric(label='**Lil Nouns of Lil Nouns DAO**', value=str(df.loc[df['Holder'] == 'Lil Nouns DAO']['NFTs'].map('{:,.0f}'.format).values[0]))
    with c2:
        st.metric(label='**Circulating Lil Nouns**', value=str('{:,.0f}'.format(df['NFTs'].agg('sum'))))
        st.metric(label='**Lil Nouns of Lil Nounders**', value=str(df.loc[df['Holder'] == 'Lil Nounders']['NFTs'].map('{:,.0f}'.format).values[0]))
    with c3:
        st.metric(label='**Average Lil Nouns per Holder**', value=str('{:,.0f}'.format(df['NFTs'].agg('sum') / df['Holders'].agg('sum'))))
        st.metric(label='**Lil Nouns of Other Holders**', value=str(df.loc[df['Holder'] == 'Other']['NFTs'].map('{:,.0f}'.format).values[0]))

    st.subheader('Distribution')

    c1, c2, c3 = st.columns(3)
    with c1:
        df = holders_holdings.sort_values('NFTs', ascending=False).reset_index(drop=True)
        df.loc[holders_holdings.index >= 7, 'Holder'] = 'Other'
        df.loc[df['Holder'].str[0] == '0', 'Holder'] = df['Holder'].str[:5] + '...' + df['Holder'].str[-5:]
        fig = px.pie(df, values='NFTs', names='Holder', title='Tokens Distribution Among Top Lil Noun Holders', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        df = holders_distribution
        fig = px.pie(df, values='Holders', names='Bucket', title='Number of Holders in Each Distribution Group', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c3:
        df = holders_distribution
        fig = px.pie(df, values='NFTs', names='Bucket', title='Lil Nouns Holding in Each Distribution Group', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    
    st.subheader('Top Holders')

    df = holders_holdings.sort_values(by='NFTs', ascending=False).head(50)
    df.loc[df['Holder'].str[0] == '0', 'Holder'] = df['Holder'].str[:5] + '...' + df['Holder'].str[-5:]
    fig = px.bar(df, x='Holder', y='NFTs', color='Holder', title='Top Lil Noun Holders')
    fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title='Number of NFTs', hovermode='x unified')
    fig.update_traces(hovertemplate='%{y:,.0f} Lil Nouns<extra></extra>')
    fig.update_xaxes(type='category', categoryorder='total ascending')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

with tab_governance:

    st.write(
        """
        Governance is the core point of interest in every DAO, which is also the case for Lil Nouns DAO.
        In this section, a comprehensive evaluation of governance on Lil Nouns DAO, proposed proposals,
        and the breakdown of votes, all extracted from on-chain data has been analyzed and presented.
        """
    )

    st.subheader('Overview')

    df = votes_overview
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric(label='**Total Number of Proposals**', value=str(df['Proposals'].map('{:,.0f}'.format).values[0]))
    with c2:
        st.metric(label='**Total Number of Unique Voters**', value=str(df['Voters'].map('{:,.0f}'.format).values[0]))
    with c3:
        st.metric(label='**Total Number of Votes**', value=str(df['Votes'].map('{:,.0f}'.format).values[0]))
    with c4:
        st.metric(label='**Average Number of Votes per Voter**', value=str(df['Votes/Voter'].map('{:,.0f}'.format).values[0]))

    st.subheader('Distribution')

    c1, c2 = st.columns(2)
    with c1:
        df = proposals_overview.groupby('Result').agg({'Proposal': 'count'}).reset_index()
        fig = px.pie(df, values='Proposal', names='Result', title='Result Share of Proposals', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        df = proposals_overview.groupby('Proposer').agg({'Proposal': 'count'}).sort_values('Proposal', ascending=False).reset_index()
        df.loc[df.index >= 10, 'Proposer'] = 'Other'
        df.loc[df['Proposer'].str[0] == '0', 'Proposer'] = df['Proposer'].str[:5] + '...' + df['Proposer'].str[-5:]
        fig = px.pie(df, values='Proposal', names='Proposer', title='Proposal Share of Proposers', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    df = votes_options.groupby('Option').agg({'Proposal': 'count', 'Voters': 'sum', 'Votes': 'sum'}).reset_index()
    c1, c2, c3 = st.columns(3)
    with c1:
        fig = px.pie(df, values='Votes', names='Option', title='Share of Votes of Each Vote Option', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        fig = px.pie(df, values='Voters', names='Option', title='Share of Voters Voting Each Vote Option', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c3:
        fig = px.pie(df, values='Proposal', names='Option', title='Share of Proposals Receiving Each Vote Option', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    st.subheader('Conclusion of Porposals')
    
    df = proposals_overview
    fig = px.bar(df, x='Proposal', y='Votes', color='Result', title='Conclusion of Each Proposal')
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Votes', hovermode='x unified')
    fig.update_traces(hovertemplate='%{y:,.0f} Votes<extra></extra>')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    df = votes_options
    fig = px.bar(df, x='Proposal', y='Votes', color='Option', custom_data=['Option'], title='Distribution of Votes for Each Proposal')
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Votes', hovermode='x unified')
    fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f} Votes<extra></extra>')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    fig = px.bar(df, x='Proposal', y='Voters', color='Option', custom_data=['Option'], title='Distribution of Voters for Each Proposal')
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Voters', hovermode='x unified')
    fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f} Voters<extra></extra>')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    st.subheader('Votes Breakdown')

    df = proposals_overview
    fig = sp.make_subplots()
    fig.add_trace(go.Bar(x=df['Proposal'], y=df['Votes'], name='Votes', hovertemplate='Votes: %{y:,.0f}<extra></extra>'))
    fig.add_trace(go.Line(x=df['Proposal'], y=df['Quorum'], name='Quorum', hovertemplate='Quorum: %{y:,.0f}<extra></extra>'))
    fig.update_layout(title_text='Number of Votes Received by Each Proposal Compared to Their Quorum', yaxis_title='Numbers', hovermode='x unified')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    fig = sp.make_subplots()
    fig.add_trace(go.Bar(x=df['Proposal'], y=df['Voters'], name='Voters', hovertemplate='Voters: %{y:,.0f}<extra></extra>'))
    fig.add_trace(go.Line(x=df['Proposal'], y=df['Votes/Voter'], name='Votes/Voter', hovertemplate='Votes/Voter: %{y:,.0f}<extra></extra>'))
    fig.update_layout(title_text='Total Number of Voters and Average Votes per Voter of Each Proposal', yaxis_title='Numbers', hovermode='x unified')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    fig = sp.make_subplots()
    fig.add_trace(go.Bar(x=df['Proposal'], y=df['Votes/Quorum'], name='Votes/Quorum', hovertemplate='Votes/Quorum: %{y:,.2f}<extra></extra>'))
    fig.add_trace(go.Line(x=df['Proposal'], y=df['Votes/NFTs'], name='Votes/NFTs', hovertemplate='Votes/NFTs: %{y:,.2f}<extra></extra>'))
    fig.update_layout(title_text='Average Votes per Quorum and Votes per NFTs of Each Proposal', yaxis_title='Numbers', hovermode='x unified')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

st.header('Conclusion')

st.write(
    """
    It has been less than a year since the Lil Nouns DAO started its activity. However, it has
    reached a steady state over the past few months, truly acting as a smaller version of Nouns
    DAO, befitting its name. New and old holders are holding their Lil Nouns, not because of
    their financial value, but because of their voting power over the decision-making on the DAO.
    Proposals are being proposed, and while the community has not been extremely engaging, those
    that participate have had considerable voting power, contributing to the path of the DAO
    moving forward.
    """
)

# Whitespace
st.write("""
    #
    #
    #
""")

# Credits
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.info('**Data Analyst: [@AliTslm](https://twitter.com/AliTslm)**', icon="????")
with c2:
    st.info('**GitHub: [@alitaslimi](https://github.com/alitaslimi)**', icon="????")
with c3:
    st.info('**Data: [Flipside Crypto](https://flipsidecrypto.xyz)**', icon="????")
with c4:
    st.info('**Bounty Program: [JokeDAO](https://www.jokedao.io)**', icon="????")
