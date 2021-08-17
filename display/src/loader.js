// from Loadr by Dimitar Christoff at https://github.com/DimitarChristoff/loadr/
let messages = 'growing puppies,giving hugs,reading books,cracking knuckles,getting a sorting hat,abracadaboasidruoshdf,getting chapters,admiring your fic,kudoing,commenting,writing,studying Mars terrain,ctrl-Z-ing,finding sign of life,three two one sleep,looking for things in the attic,herding rodents,feeding robots,eating lunch,eating brunch,eating dinner,getting ink,praying for a miracle,hammering nails,setting up printer,pressing submit,petting dogs,losing Nemo,building Death Star,finding obi-wan,time-traveling'.split(',');

/**
 * @class loader
 */
class loader {

  /**
   * @constructs loader
   * @param {HTMLElement=} element
   * @param {Object=} options
   */
  constructor(element = null, options = {}){
    /**
     *
     * @type {{delay: number, before: string, after: string}}
     */
    Object.assign(this.options = {
      delay: 2500,
      before: '',
      after: '...'
    }, options);

    element && (this.element = element);
  }

  get messages(){
    return messages.slice();
  }

  set messages(array){
    messages = Array.from(array);
  }

  /**
   * Starts looping messages into an element
   * @returns {loader}
   */
  start(){
    this._setLoadMessage();
    this.timer = setInterval(() =>{
      this._setLoadMessage();
    }, this.options.delay);

    return this;
  }

  /**
   * Stops looping of messages
   * @returns {loader}
   */
  stop(){
    clearInterval(this.timer);

    return this;
  }

  /**
   * Just return a message that is different from the last message returned.
   * @param {*=} r
   * @returns {String}
   */
  get(r){
    const { before, after } = this.options;
    while ((r = this._rand()) == this.last);

    return before + messages[this.last = r] + after;
  }

  /**
   * Internal loader of a new message that is different from last one.
   * @param {*=} o
   * @returns {loader}
   * @private
   */
  _setLoadMessage(){
    this.element && (this.element.innerHTML = this.get());

    return this;
  }

  /**
   * Generates a random number within the size of the messages
   * @returns {number}
   * @private
   */
  _rand(){
    return ~~(Math.random() * messages.length);
  }
}

export default loader;