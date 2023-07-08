import logging
from .buttons import button,bkr_qilish,qabul_qilinsin_mi
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
from .calculate import calculate
from datetime import datetime
from .save import save_obj
from ...models import Rulon
from django.core.management.base import BaseCommand
logging.basicConfig(level=logging.INFO)


API_TOKEN = '6133087058:AAGBZySk9p_mPZWDH4T2aSyRzgF56fwYWA4'
list_users = [5334048344,641437735,762928595,53233766]
class Command(BaseCommand):
    reply_message_id = 0
    def handle(self, *args,**options):
        
        bot = Bot(token=API_TOKEN)
        
        # For example use simple MemoryStorage for Dispatcher.
        storage = MemoryStorage()
        dp = Dispatcher(bot, storage=storage)


        # States
        class Form(StatesGroup):
            big_pastel = State()  # Will be represented in storage as 'Form:big_pastel'
            small_pastel = State()  # Will be represented in storage as 'Form:small_pastel'
            nalichka = State()  # Will be represented in storage as 'Form:nalichka'
            gastiniy = State()
        

        class RulonState(StatesGroup):
            agree = State()
            rulon = State()
            

        try:


            @dp.message_handler(commands='start')
            async def cmd_start(message: types.Message):
                """
                Conversation's entry point
                """
                
                if message.chat.id not in list_users:
                    await message.answer("Sizga kirish taqiqlangan!")
                    return
                else:
                    await message.reply("Iltimos tugmalardan birni tanglang?",reply_markup=button)
                    
            #RULON
                    @dp.message_handler(Text(startswith='Rulon'))
                    async def cmd_start(message: types.Message):
                        await RulonState.agree.set()
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                        markup.add("Xa", "Bekor Qilish")
                        await message.reply('Eski rulon tugadimi?',reply_markup=markup)


            #BEKOR QILISH
                    @dp.message_handler(Text(startswith='Bekor Qilish'),state='*')
                    @dp.message_handler(Text(equals='Bekor Qilish', ignore_case=True), state='*')
                    async def cancel_handler(message: types.Message, state: FSMContext):
                        """
                        Allow user to cancel any action
                        """
                        current_state = await state.get_state()
                        if current_state is None:
                            return
                        logging.info('Cancelling state %r', current_state)
                        await state.finish()
                        await message.reply('Bekor qilindi.',reply_markup=button)


            #NOT SELECTED
                    @dp.message_handler(lambda message: message.text not in ["Xa", "Bekor Qilish"], state=RulonState.agree)
                    async def process_agree_invalid(message: types.Message):

                        return await message.reply("Tugmalardan birini tanlang!")

            #IS NEW RULON       
                    @dp.message_handler(state=RulonState.agree)
                    async def process_rulon(message: types.Message, state: FSMContext):

                        if message.text == 'Xa':
                            await RulonState.next()
                            await message.answer('Yangi rulon sonini kiriting',reply_markup=bkr_qilish)

                        elif message.text == 'Bekor qilish':
                            await bot.send_message("bekor qilindi",reply_markup=button)
                            await state.finish()


            #NUMBER OF RULON
                    @dp.message_handler(lambda message: message.text.isdigit(),state=RulonState.rulon)
                    async def process_gender(message: types.Message, state: FSMContext):

                        async with state.proxy() as data:
                            data['rulon'] = int(message.text)
                            
                        Rulon.create_rulon_obj(data['rulon'])
                        await bot.send_message(
                            message.chat.id,
                            md.text(
                                md.text('RULON:',md.bold(data['rulon']))
                                
                            ),
                            reply_markup=button,
                            parse_mode=ParseMode.MARKDOWN,
                        )
                        await message.answer("Qabul qilindi!")
                        await state.finish()




            #XISOBOT
                    @dp.message_handler(Text(startswith='Xisobot'))
                    async def cmd_start(message: types.Message):

                        latest_rulon = Rulon.objects.last().information_pastel.path
                        with open(latest_rulon, "rb") as file:
                            document = types.InputFile(file)
                            await bot.send_document(message.chat.id,document)


            #PASTEL
                    @dp.message_handler(Text(startswith='Pastel'))
                    async def cmd_start(message: types.Message):
                    
                        # Set state
                        await Form.big_pastel.set()
                        reply_message = await message.reply(md.text("kotta pastel sonini kirting",md.bold("faqat son")),reply_markup=bkr_qilish)
                        self.reply_message_id = reply_message.message_id
                    
        


            #XA
                    @dp.message_handler(Text(startswith='Xa'),state='*')
                    @dp.message_handler(Text(equals='Xa', ignore_case=True), state='*')
                    async def agree_handler(message: types.Message, state: FSMContext):

                        async with state.proxy() as data:
                            message_to_user = save_obj(data)
                        await message.answer(message_to_user,reply_markup=button)
                        await state.finish()


            #GOTTA BE DIGIT
                    @dp.message_handler(lambda message: not message.text.isdigit(), 
                                        state=[Form.big_pastel,
                                            Form.small_pastel,
                                            Form.gastiniy,
                                            Form.nalichka])
                    
                    async def process_number_invalid(message: types.Message):
                        return await message.reply("Faqat son kiriting (digits only)")





                    @dp.message_handler(lambda message: message.text.isdigit(), state=Form.big_pastel)
                    async def process_big_pastel(message: types.Message, state: FSMContext):
                        # Update state and data
                        await Form.next()
                        await state.update_data(big_pastel=int(message.text),reply_markup=bkr_qilish)
                        await bot.delete_message(chat_id=message.chat.id,message_id=self.reply_message_id)
                        reply_message= await message.answer("kichkina pastel sonini kirting (faqat son)",reply_markup=bkr_qilish)
                        self.reply_message_id =reply_message.message_id

                        print(message.chat.id,"users")
                    




                    @dp.message_handler(lambda message: message.text.isdigit(), state=Form.small_pastel)
                    async def process_small_pastel(message: types.Message, state: FSMContext):
                        # Update state and data
                        await Form.next()
                        await state.update_data(small_pastel=int(message.text))
                        await bot.delete_message(chat_id=message.chat.id,message_id=self.reply_message_id)

                        reply_message=await message.answer("nalichka pastel sonini kirting (faqat son)",reply_markup=bkr_qilish)
                        self.reply_message_id =reply_message.message_id


                    @dp.message_handler(lambda message: message.text.isdigit(), state=Form.nalichka)
                    async def process_nalichka(message: types.Message, state: FSMContext):
                        # Update state and data
                        await Form.next()
                        await state.update_data(nalichka=int(message.text))
                        await bot.delete_message(chat_id=message.chat.id,message_id=self.reply_message_id)

                        reply_message = await message.answer("gastiniy pastel sonini kirting (faqat son)",reply_markup=bkr_qilish)
                        self.reply_message_id =reply_message.message_id



                    @dp.message_handler(lambda message: message.text.isdigit(),state=Form.gastiniy)
                    async def process_gender(message: types.Message, state: FSMContext):
                        async with state.proxy() as data:
                            data['gastiniy'] = int(message.text)
                            await bot.delete_message(chat_id=message.chat.id,message_id=self.reply_message_id)

                            # Remove keyboard
                            #markup = types.ReplyKeyboardRemove()


                            
                            kunlik_pul={"kunlik_pul":calculate(data)}

                            data.update(kunlik_pul)
                            
                            current_time = datetime.now()
                            # And send message
                            await bot.send_message(
                                message.chat.id,
                                md.text(
                                    md.text('sana:',md.bold(f"{current_time.day}/{current_time.month}/{current_time.year}")),
                                    md.text('kotta pastel:', md.bold(data['big_pastel'])),
                                    md.text('kichkina pastel:', md.bold(data['small_pastel'])),
                                    md.text('nalichka:', md.bold(data['nalichka'])),
                                    md.text('gastiniy:', md.bold(data['gastiniy'])),
                                    md.text('umumiy xisob:', md.bold(data['kunlik_pul']),'sum'),
                                    
                                    sep='\n',
                                ),
                                reply_markup=qabul_qilinsin_mi,
                                parse_mode=ParseMode.MARKDOWN,
                            )

                            await message.answer("Qabul qilinsinmi?")
                        # Finish conversation
                        



                    
                
            
            executor.start_polling(dp, skip_updates=True)
        except:
            print("Xatolik keti!")

a = Command()
a.handle()